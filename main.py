import argparse
import sys

import client
import server

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--client', dest="is_client", const=True, action='store_const', help="start the client",
                    default=False)
parser.add_argument('--server', dest="is_server", const=True, action='store_const', help="start the server",
                    default=False)
args = parser.parse_args()
if args.is_client:
    print("Starting client...")
    client.send_message()
elif args.is_server:
    print("Starting server...")
    server.start_listening()
else:
    print("pass type of app", file=sys.stderr)
