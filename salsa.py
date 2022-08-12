import random
from struct import Struct, pack
from copy import deepcopy

little_u64 = Struct("<Q")
little16_i32 = Struct("<16i")  # 16 little-endian 32-bit signed ints.
little8_i32 = Struct("<8i")  # 04 little-endian 32-bit signed ints.
little4_i32 = Struct("<4i")  # 04 little-endian 32-bit signed ints.
little2_i32 = Struct("<2i")  # 02 little-endian 32-bit signed ints.

sigma = "expand 32-byte k"


def generate_matrix(key, iv, position):
    key_arr = little8_i32.unpack(key)
    iv_arr = little2_i32.unpack(iv)

    return [
        0x61707865, 0x3320646e, 0x79622d32, 0x6b206574,
        key_arr[0], key_arr[1], key_arr[2], key_arr[3],
        key_arr[4], key_arr[5], key_arr[6], key_arr[7],
        position, 0, iv_arr[0], iv_arr[1],
    ]


def xor(a, b):
    return a ^ b


def bxor(b1, b2):  # use xor for bytes
    return little16_i32.pack(*[xor(x, y) for x, y in zip(little16_i32.unpack(b1), little16_i32.unpack(b2))])


def rot32(w, left):
    """ rot32 32-bit word left by left or right by -left
        without creating a Python long.
        Timing depends on left but not on w.
    """
    left &= 31  # which makes nLeft >= 0
    if left == 0:
        return w

    # Note: now 1 <= nLeft <= 31.
    #     RRRsLLLLLL   There are nLeft RRR's, (31-nLeft) LLLLLL's,
    # =>  sLLLLLLRRR   and one s which becomes the sign bit.
    RRR = (((w >> 1) & 0x7fffFFFF) >> (31 - left))
    sLLLLLL = -((1 << (31 - left)) & w) | (0x7fffFFFF >> left) & w
    return RRR | (sLLLLLL << left)


def add32(a, b):
    """ Add two 32-bit words discarding carry above 32nd bit,
        and without creating a Python long.
        Timing shouldn't vary.
    """
    lo = (a & 0xFFFF) + (b & 0xFFFF)
    hi = (a >> 16) + (b >> 16) + (lo >> 16)
    return (-(hi & 0x8000) | (hi & 0x7FFF)) << 16 | (lo & 0xFFFF)


def quarter_round(x, a, b, c, d):
    x[a] += x[b];
    x[d] = rot32(x[d] ^ x[a], 16)
    x[c] += x[d];
    x[b] = rot32(x[b] ^ x[c], 12)
    x[a] += x[b];
    x[d] = rot32(x[d] ^ x[a], 8)
    x[c] += x[d];
    x[b] = rot32(x[b] ^ x[c], 7)


def _do_salsa20_round(x):
    quarter_round(x, 0, 4, 8, 12)
    quarter_round(x, 1, 5, 9, 13)
    quarter_round(x, 2, 6, 10, 14)
    quarter_round(x, 3, 7, 11, 15)
    quarter_round(x, 0, 5, 10, 15)
    quarter_round(x, 1, 6, 11, 12)
    quarter_round(x, 2, 7, 8, 13)
    quarter_round(x, 3, 4, 9, 14)
    return x


def sum_matrix(a, b):
    return [add32(x, y) for x, y in zip(a, b)]


def word_to_bytes(words):
    return little16_i32.pack(*words)


def generate_salsa20_stream(key, nonce):
    block_number = 0
    while True:
        matrix = generate_matrix(key, nonce, block_number)
        temp = deepcopy(matrix)
        for _ in range(10):
            temp = _do_salsa20_round(temp)
        matrix = sum_matrix(temp, matrix)
        yield word_to_bytes(matrix)
        block_number += 1


def salsa_20_xor_bytes(content: bytes, key: bytes):
    # content = content.encode('unicode_escape')
    buffer = b''
    chunk_size = 64  # 64 bytes
    salsa_generator = generate_salsa20_stream(key, b'f' * 8)
    total_chunks = len(content) // chunk_size

    for i in range(total_chunks):
        chunk = content[i * chunk_size:(i + 1) * chunk_size]
        salsa_stream = next(salsa_generator)[0:len(chunk)]
        buffer += bxor(chunk, salsa_stream)
        print("XOReando el chunk {0} de {1}, el buffer es de: {2}".format(i, total_chunks, len(buffer)))

    return buffer


def encrypt(key: str, inputString: bytes) -> bytes:
    return salsa_20_xor_bytes(inputString, b'f' * 32)


def decrypt(key: str, inputString: bytes) -> bytes:
    return salsa_20_xor_bytes(inputString, b'f' * 32)
