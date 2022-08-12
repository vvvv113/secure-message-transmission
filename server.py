import socket
# todo get from args
import time

import rsa
from diffie_hellman import DiffieHellman
from hasher import jenkins_one_at_a_time_hash
from helpers import int_to_bytes, int_from_bytes, stream_encryptor
from prime_generator import prime_number, prim_roots

HOST = "127.0.0.1"
PORT = 11300


def start_listening():
    print("Generating shared prime...")
    shared_prime = prime_number()
    print("Generating shared prim root...")
    prim_root = prim_roots(shared_prime)
    print("Generating intermediate key...")
    crypto_provider = DiffieHellman(shared_prime, prim_root)
    intermediate_key_to_send = crypto_provider.calculate_intermediate_key()
    public, private = rsa.generate_keypair(prime_number(), prime_number())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            print("Starting listening on", HOST, PORT)
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    print("Sending prime:", shared_prime)
                    conn.sendall(int_to_bytes(shared_prime))
                    print("Sending primitive root", prim_root)
                    conn.sendall(int_to_bytes(prim_root))
                    print("Sending my intermediate key...")
                    conn.sendall(int_to_bytes(intermediate_key_to_send))
                    print("Receiving intermediate key...")
                    intermediate_key = int_from_bytes(conn.recv(512))
                    crypto_provider.generate_full_key(intermediate_key)
                    time.sleep(1)

                    remote_public_1 = int(crypto_provider.decrypt_message(conn.recv(512)).decode("utf-8"))
                    time.sleep(1)
                    conn.sendall(crypto_provider.encrypt_message(str(public[0]).encode("utf-8")))

                    time.sleep(1)
                    remote_public_2 = int(crypto_provider.decrypt_message(conn.recv(512)).decode("utf-8"))
                    time.sleep(1)
                    conn.sendall(crypto_provider.encrypt_message(str(public[1]).encode("utf-8")))
                    remote_public = remote_public_1, remote_public_2
                    print("remote public rsa key", remote_public_1, remote_public_2)

                    while True:
                        received_message = stream_encryptor.decrypt("rc4key",
                                                                    crypto_provider.decrypt_message(conn.recv(4096)))
                        received_message = received_message.decode("utf-8", errors='ignore').split(chr(0))
                        decrypted_message = rsa.decrypt(remote_public, received_message[0])
                        message = received_message[-1]
                        if jenkins_one_at_a_time_hash(message) != decrypted_message:
                            print("RSA digital signature error!", jenkins_one_at_a_time_hash(message), message,
                                  decrypted_message)
                            break
                        print("decrypted message:", message)

                        rsa_encrypted = rsa.encrypt(private, jenkins_one_at_a_time_hash(message))
                        message_to_encrypt = [rsa_encrypted, message]
                        conn.sendall(crypto_provider.encrypt_message(
                            stream_encryptor.encrypt("rc4key", chr(0).join(message_to_encrypt).encode("utf-8")))
                        )
        except KeyboardInterrupt:
            s.close()
