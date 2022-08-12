import random


class DiffieHellman:
    def __init__(self, shared_prime, prim_root):
        self.sharedPrime = shared_prime  # p
        self.sharedBase = prim_root  # g
        self.full_key = None
        self.secret = random.getrandbits(10)

    def generate_full_key(self, intermediate_key):
        print("generating full key...")
        full_key = (intermediate_key ** self.secret) % self.sharedPrime
        print("full key generated:", full_key)
        self.full_key = full_key

    def calculate_intermediate_key(self):
        return (self.sharedBase ** self.secret) % self.sharedPrime

    def encrypt_message(self, message: bytes) -> bytes:
        encrypted_message = b""
        key = self.full_key
        for c in message:
            encrypted_message += chr(c + key).encode()
        return encrypted_message

    def decrypt_message(self, encrypted_message: bytes) -> bytes:
        decrypted_message = b""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(c - key).encode()
        return decrypted_message
