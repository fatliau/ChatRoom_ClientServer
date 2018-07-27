import argparse
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = ""
    prefix = ""

    while True:
        msg = client.recv(BUFSIZ)

        if not msg is None:
            msg = msg.decode("utf-8")

        if msg == "":
            msg = "{QUIT}"

        # Avoid messages before registering
        if msg.startswith("{ALL}") and name:
            new_msg = msg.replace("{ALL}", "{MSG}"+prefix)
            send_message(new_msg, broadcast=True)
            continue

        if msg.startswith("{REGISTER}"):
            name = msg.split("}")[1]
            welcome = '{MSG}Welcome %s!' % name
            send_message(welcome, destination=client)
            msg = "{MSG}%s has joined the chat!" % name
            send_message(msg, broadcast=True)
            clients[client] = name
            prefix = name + ": "
            send_clients()
            continue

        if msg == "{QUIT}":
            client.close()
            try:
                del clients[client]
            except KeyError:
                pass
            if name:
                send_message("{MSG}%s has left the chat." % name, broadcast=True)
                send_clients()
            break

        # Avoid messages before registering
        if not name:
            continue
        # We got until this point, it is either an unknown message or for an
        # specific client...
        try:
            msg_params = msg.split("}")
            dest_name = msg_params[0][1:] # Remove the {
            dest_sock = find_client_socket(dest_name)
            if dest_sock:
                send_message(msg_params[1], prefix=prefix, destination=dest_sock)
            else:
                print("Invalid Destination. %s" % dest_name)
        except:
            print("Error parsing the message: %s" % msg)


def send_clients():
    send_message("{CLIENTS}" + get_clients_names(), broadcast=True)


def get_clients_names(separator="|"):
    names = []
    for _, name in clients.items():
        names.append(name)
    return separator.join(names)


def find_client_socket(name):
    for cli_sock, cli_name in clients.items():
        if cli_name == name:
            return cli_sock
    return None


def send_message(msg, prefix="", destination=None, broadcast=False):
    send_msg = bytes(prefix + msg, "utf-8")
    if broadcast:
        """Broadcasts a message to all the clients."""
        for sock in clients:
            sock.send(send_msg)
    else:
        if destination is not None:
            destination.send(send_msg)


clients = {}
addresses = {}

parser = argparse.ArgumentParser(description="Chat Server")
parser.add_argument(
    '--host',
    help='Host IP',
    default="127.0.0.1"
)
parser.add_argument(
    '--port',
    help='Port Number',
    default=33002
)

server_args = parser.parse_args()


HOST = server_args.host
PORT = int(server_args.port)
BUFSIZ = 2048
ADDR = (HOST, PORT)

stop_server = False

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("Server Started at {}:{}".format(HOST, PORT))
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except KeyboardInterrupt:
        print("Closing...")
        ACCEPT_THREAD.interrupt()
