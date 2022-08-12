import socket
import time

import rsa
from diffie_hellman import DiffieHellman
# todo get from args
from hasher import jenkins_one_at_a_time_hash
from helpers import int_from_bytes, int_to_bytes, stream_encryptor
from prime_generator import prime_number

HOST = "127.0.0.1"
PORT = 11300


def send_message():
    while True:
        p, q = prime_number(), prime_number()
        if p != q:
            break

    public, private = rsa.generate_keypair(p, q)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Receiving prime...")
        shared_prime = int_from_bytes(s.recv(512))
        print("Received:", shared_prime)
        print("Receiving primitive root...")
        prim_root = int_from_bytes(s.recv(512))
        crypto_provider = DiffieHellman(shared_prime, prim_root)
        print("Receiving intermediate key...")
        intermediate_key = int_from_bytes(s.recv(512))
        time.sleep(3)
        print("Sending my intermediate key...")
        s.sendall(int_to_bytes(crypto_provider.calculate_intermediate_key()))
        crypto_provider.generate_full_key(intermediate_key)

        time.sleep(1)
        print("Sending rsa public key...")
        s.sendall(crypto_provider.encrypt_message(str(public[0]).encode("utf-8")))
        remote_public_1 = int(crypto_provider.decrypt_message(s.recv(512)).decode("utf-8"))
        s.sendall(crypto_provider.encrypt_message(str(public[1]).encode("utf-8")))
        remote_public_2 = int(crypto_provider.decrypt_message(s.recv(512)).decode("utf-8"))
        remote_public = remote_public_1, remote_public_2
        while True:
            message = input("Введите сообщение:")
            rsa_encrypted = rsa.encrypt(private, jenkins_one_at_a_time_hash(message))

            message_to_encrypt = [rsa_encrypted, message]
            s.sendall(
                crypto_provider.encrypt_message(
                    stream_encryptor.encrypt("rc4key", chr(0).join(message_to_encrypt).encode("utf-8"))
                ))

            received_message = stream_encryptor.decrypt("rc4key", crypto_provider.decrypt_message(s.recv(4096)))
            received_message = received_message.decode("utf-8", errors='ignore').split(chr(0))
            decrypted_message = rsa.decrypt(remote_public, received_message[0])

            message = received_message[-1]
            if jenkins_one_at_a_time_hash(message) != decrypted_message:
                print("RSA digital signature error!")
                break
            print(message)
