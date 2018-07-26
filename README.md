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
- unlimited remaking coonection
### Chat Room tab
- message sending by either push GUI button or press keyboard enter
- clear the LineEdit widget after each entering
- real-time message display
- message column always scroll down to the newest message
- private message shows onto both sender and receiver, with color
- rael-time update for combobox and attendance list at receiving server broadcat
- once the receiver left before the private message sent, dispaly "Not Delivered"
- window expanding space is preferd for message column

