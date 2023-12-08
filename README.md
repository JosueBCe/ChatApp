# Overview
This is a chat app that enables more than one user to interact each other, sharing real time messages and making them able to edit and delete their own messages

This is a server side rendering application, to start the server, first you need to run this command to install all the necessary packages: 

``` pip install -r requirements.txt ```

then run this command to start the server: 

```  python -m uvicorn main:app --reload```


[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

This application follows the client/server configuration model, where clients connect to each other through a server to send and receive messages.

## How it Works

Here's a step-by-step overview of how the application works:

1. Both clients connect to the server.
2. Client 1 wants to send a message to Client 2.
3. Client 1 sends the message to the server using the following message format: `create:${client_id}:${message}:${user_name}`. The `client_id` is the identifier of Client 1, `message` is the content of the message, and `user_name` is the name of the sender. This message format is typically submitted through a form in the frontend.
4. The server receives the message from Client 1.
5. The server broadcasts the message to all connected clients.
6. Client 2 receives the message and displays it. The application differentiates between messages sent by Client 1 and Client 2 by using different colors and alignment. Sender messages are aligned to the right, while receiver messages are aligned to the left.

## Network Communication

The application uses the Transmission Control Protocol (TCP) for network communication. TCP provides reliable, ordered, and error-checked delivery of messages, using port 80 for HTTP and port 443 for HTTPS. 

## Development Environment

To develop this software, the following tools were used:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance), web framework for building APIs with Python.
- [Jinja2](https://jinja.palletsprojects.com/): A popular templating engine for Python used to generate dynamic HTML pages.
- [httpx](https://www.python-httpx.org/): A full-featured HTTP client library for Python that supports asynchronous requests.
- [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket): A communication protocol that provides full-duplex communication channels over a single TCP connection.

### Programming Language and Libraries

The software is developed using the Python programming language.
In this project, the following libraries were used:
- `load_dotenv()`: A function used to load environment variables from a .env file.
- `FastAPI`: A web framework used for building APIs and web applications.
- `Jinja2Templates`: A library for rendering HTML templates.
- `httpx`: A library used for making HTTP requests.
- `WebSocket`: A library used for establishing WebSocket connections and handling real-time communication.

These libraries provide the necessary functionality to handle HTTP requests, WebSocket connections, and render dynamic HTML templates within the application.

# Useful Websites
* [CISCO Course (Complete Serie)](https://www.youtube.com/watch?v=oIRkXulqJA4&list=PLIhvC56v63IJVXv0GJcl9vO5Z6znCVb1P&index=7&ab_channel=NetworkChuck)
* [Computer Networking (Deepdive)](https://www.youtube.com/watch?v=6G14NrjekLQ&t=627s&ab_channel=LiveOverflow)
* [Computer Networks](https://www.youtube.com/watch?v=3QhU9jd03a0&t=639s&ab_channel=CrashCourse)
* [FastAPI + Github OAuth](https://www.youtube.com/watch?v=Pm938UxLEwQ&ab_channel=WillEstes) 
* [WebSockets in 100 Seconds & Beyond with Socket.io](https://www.youtube.com/watch?v=1BfCnjr_Vjg&ab_channel=Fireship) 
* [AWS Networking Basics For Programmers | Hands On](https://www.youtube.com/watch?v=2doSoMN2xvI&t=1s&ab_channel=TravisMedia) 
* [WebSockets in 100 Seconds & Beyond with Socket.io](https://www.youtube.com/watch?v=1BfCnjr_Vjg&ab_channel=Fireship) 

# Future Work

* Add Video Chatting option
* Add Google Login 
* Add JWT authentication and authorization 
* Improve styles 
* Display edit and delete buttons in a popup window (like whatsapp)