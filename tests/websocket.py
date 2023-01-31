import asyncio
from socketio import AsyncClient

async def test_socketio_server():
    # Create a client that connects to the server
    sio = AsyncClient()
    token = 'test1_token'
    try:
        await sio.connect('http://localhost:8000/', auth={'token': token})
    except Exception as e:
        print(f"An error occurred while connecting: {e}")

    # Send a message to the server
    await sio.emit('join', {'room': 'test_room'})
    await sio.emit('message_to_room', {'room': 'test_room', 'message': 'Hello World!'})

    
        

    @sio.on('message_to_room')
    def on_message(data):
        print('I received a message!', data)
    # Start loop
    await sio.wait()
# Run the tests
asyncio.run(test_socketio_server())