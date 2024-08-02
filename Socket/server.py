import socket
import threading

host = '127.0.0.1'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Server running on {host}:{port}")

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_message(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"chatbot: {username} has disconnected.".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def recv_connections():
    while True:
        client, address = server.accept()
        
        client.send("@username".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        
        clients.append(client)
        usernames.append(username)
        
        print(f'{username} has connected from {str(address)}')
        
        message = f'chatbot: {username} has joined the chat!'.encode('utf-8')
        broadcast(message, client)
        client.send('Connected to the server.'.encode('utf-8'))
        
        thread = threading.Thread(target=handle_message, args=(client,))
        thread.start()

recv_connections()
