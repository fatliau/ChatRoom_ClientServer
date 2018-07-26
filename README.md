# Client User Interface for Chat Server

## Project Information



## Environment Requirement
- Python 3.6
- PyQt5

## Run the Server
```
python server.py --host 127.0.0.1 --port 33002
```
## Run the Client
```
python client.py
```
## Features
### General Design
- tabs for individual function: Home page or chat room
- chat room tab disabled until connection setup
### Home tab
- foolproof on connection/disconnection button: name column required, prevent repeat connecting/disconnecting
### Chat Room tab
- enter a line can be done by either push GUI button or press keyboard enter
- message column always scroll down to the newest message
- private message show to both sender and receiver
- combobox and room attendance list are updated real-time at receiving server broadcat
- Expanding the window, message column is preferd for space increase

