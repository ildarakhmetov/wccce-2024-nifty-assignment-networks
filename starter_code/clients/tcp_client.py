# TCP client program (Python 3 version)

import socket
import sys

MAX_LINE = 256
SERVER_PORT = 10393


def main():
    # Get server host from command line
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <server_host>", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get server address and connect
    try:
        server_address = (host, SERVER_PORT)
        s.connect(server_address)
    except socket.error as e:
        print(f"tcp_client: connect error: {e}", file=sys.stderr)
        s.close()
        sys.exit(1)

    print("Connected to the server. Type messages, press enter to send, 'ctrl+d' to quit.")

    # Send data
    try:
        while True:
            # Read line from stdin
            line = input()
            if line:
                # Ensure the line is within the buffer limit and ends with a newline and null character
                line = line[:MAX_LINE-2] + '\n\0'
                s.sendall(line.encode())
            # Get response from server
            data = s.recv(MAX_LINE)
            print(f"Server says: {data.decode()[0:-2]}")
    except EOFError:
        # End of file (ctrl+d) was pressed
        pass
    finally:
        print("tcp_client: Connection closed by client.")
        s.close()


if __name__ == "__main__":
    main()
