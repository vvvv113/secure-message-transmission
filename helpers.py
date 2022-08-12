from typing import Optional

import rc4
import salsa


def int_to_bytes(number: int) -> bytes:
    return number.to_bytes(length=512, byteorder='big', signed=True)


def int_from_bytes(binary_data: bytes) -> Optional[int]:
    return int.from_bytes(binary_data, byteorder='big', signed=True)


stream_encryptor = salsa
