# Global variables
state = [0] * 256
p = q = 0


def setKey(key):
    global p, q, state
    state = [n for n in range(256)]
    p = q = j = 0
    for i in range(256):
        if len(key) > 0:
            j = (j + state[i] + key[i % len(key)]) % 256
        else:
            j = (j + state[i]) % 256
    state[i], state[j] = state[j], state[i]


def byteGenerator():
    global p, q, state
    p = (p + 1) % 256
    q = (q + state[p]) % 256
    state[p], state[q] = state[q], state[p]
    return state[(state[p] + state[q]) % 256]


def encrypt(key: str, inputString: str) -> str:
    setKey(string_to_list(key))
    return ''.join([chr(ord(p) ^ byteGenerator()) for p in inputString])


def decrypt(key: str, inputString: str) -> str:
    setKey(string_to_list(key))
    return "".join([chr(ord(c) ^ byteGenerator()) for c in inputString])


def intToList(inputNumber):
    inputString = "{:02x}".format(inputNumber)
    return [int(inputString[i:i + 2], 16) for i in range(0, len(inputString), 2)]


def string_to_list(inputString):
    return [ord(c) for c in inputString]
