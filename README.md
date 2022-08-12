# secure-message-transmission
secure message transmission by creating your own tunnel to protect data transfer from client to server

Client-server application. All algorithms are implemented manually and are available in named files.
When the connection is established, the server and the client receive a shared secret key using the Diffie-Hellman protocol:
1. The server and client generate 128-bit private keys a and b.
2. The server generates a large prime number p and g, which is a primitive root modulo p. Also calculate the public key of A.
3. Sends p, g and A to the client.
4. The client calculates the public key B and sends it to the server.
5. Both sides calculate the shared secret key K.

The RSA digital signature is used to protect against MITM attacks:
1. The client sends its public key {e, n}
2. Hash messages using the Bob Jenkins hash function
3. Create a signature using the private key {d, n}
4. Add a signature to the beginning of the message.

After setting the shared secret and adding the signature, data exchange begins using encryption using the symmetric RC4 and salsa algorithm (optionally, you can choose the encryption option, only you need to change the data type at the message input/output):
