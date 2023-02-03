# Mango chat API
This is a simple chat API that allows you to send and receive messages from a chat room. It is built using FastAPI, PostgreSQL and SocketIO.

## How to run
1. Clone the repository  
1.1 If you want to modify credentials, change them in .env file  
2. Launch docker-compose up --build -d  
3. Go to http://localhost:5000/docs to see the API documentation  
4. For using socketIO, go to http://localhost:5000/ws/socket.io/  
4.1 If you using postman, add new SocketIO request and set the handshake path from /socket.io to /ws/socket.io
5. Create user and get access token from /auth/refresh endpoint. You must paste photo as base64 string, so you can use /user/photo_to_base64 endpoint to convert your photo to base64 string.  
*be careful with pasing base64 string, it must be with one double quote*  
*also don't upload big files, you got too big string.*  
5.1 To access you photo you can use /static/{photo}/{size}.jpeg for original or /static/{photo}/{size}.webp for other sizes, where {photo} is your photo name and {size} is one of the following:  **original, 400x400, 100x100, 50x50**  
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

## How to run tests
1. Clone the repository
2. Launch docker-compose up --build -d
3. Launch docker exec mango_chat_web_1 /bin/bash -c "python -m pytest tests/tests.py"

## Couple words about architecture and structure
This API is built using FastAPI, PostgreSQL and SocketIO.
- FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- PostgreSQL is a powerful, open source object-relational database system.
- SocketIO is a library that enables real-time, bidirectional and event-based communication between the browser and the server.

Server is separated into 10 parts:
- **Routers** - contains all routers and endpoints, handling requests and responses, http errors, etc.
- **Services** - contains logic for working with database.
- **Schemas** - contains all schemas for validation.
- **Models** - contains all models for database.
- **Exceptions** - contains all custom exceptions.
- **Repositories** - contains all repositories for working with database.
- **Jwt** - contains all logic for working with JWT.
- **Sockets** - contains all logic for working with socketIO.
- **Tests** - contains all tests for API.
- **Database** - contains alembic configuration and migrations.

## How does logging work
This API uses loguru for logging. It is a library which aims to bring enjoyable logging in Python. It's simple, efficient, extensible, and compatible with the standard library.
Logs are stored in assets/logs folder.

## Conclusion
I hope you will enjoy using this API. If you have any questions, feel free to contact me.

Telegram: [@foxyess2020](https://t.me/foxyess2020)
Gmail: [dmpyatyi@gmail.com](mailto:dmpyatyi@gmail.com)
