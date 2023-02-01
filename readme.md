# Mango chat API
This is a simple chat API that allows you to send and receive messages from a chat room. It is built using FastAPI, PostgreSQL and SocketIO.

## How to run
1. Clone the repository  
1.1 If you want to modify credentials, change them in .env file  
2. Launch docker-compose up --build -d  
3. Go to http://localhost:5000/docs to see the API documentation  
4. For using socketIO, go to http://localhost:5000/ws/socket.io/  
4.1 If you using postman, add new SocketIO request and set the Handshale path from /socket.io to /ws/socket.io
5. Create user and get access token from /auth/refresh endpoint  
6. To access socketIO you should add auth header with access token  
7. For creating chat send **create_chat** event with json:  
```json
{
    "chat": {
        "name": "Paste your chat name here",
        "is_group": false, // true if you want to create group chat
        "members_array": [1,2] // array of user ids
    }
}
```
7.1 To receive chat id subscribe to **chat_created** event   
8. To send message send **send_message** event with json:  
```json
{
    "message":{
        "chat_id": 3,
        "content": "How are you?!",
        "message_type": "text"
    }
}
```
8.1 Available message types:  text, html, json, xml, binary, image, pdf, csv, excel, word, zip, gzip, tar, audio, video, yaml, javascript, css, svg, markdown, protobuf, avro, parquet, orc  
8.2 To receive messages subscribe to **new_message** event  
9. To like message send **toggle_like_message** event with json:  
```json
{
    "message":{
        "id": 18
    }
}
```
9.1 To receive liked message subscribe to **message_liked** event   
10. To pin chat send **toggle_chat_pin** event with json:   
```json
{
    "chat":{
        "id": 3
    }
}
```
10.1 To receive pinned chat subscribe to **chat_pinned** event   
10.2 To receive unpinned chat subscribe to **chat_unpinned** event   