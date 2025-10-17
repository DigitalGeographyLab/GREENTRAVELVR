import socket

def tcp_client(host='localhost', port=15010):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect the socket to the server's port
        client_socket.connect((host, port))
        print(f'Connected to server at {host}:{port}')
        
        while True:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                # No more data from the server
                break
            print('Received:', data.decode())
    
    except ConnectionRefusedError:
        print(f"Could not connect to server at {host}:{port}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        client_socket.close()
        print('Connection closed')

# Run the TCP client
tcp_client()
