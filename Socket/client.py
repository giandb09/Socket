import socket
import threading

username = input('Enter your username: ')

host = '127.0.0.1'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((host, port))
except ConnectionRefusedError:
    print("Connection refused. Please make sure the server is running.")
    exit()

def recv_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '@username':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write_message():
    while True:
        message = f"{username}: {input('')}"
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred while sending the message: {e}")
            client.close()
            break

recv_thread = threading.Thread(target=recv_message)
recv_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()
