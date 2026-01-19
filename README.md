# thread-safe-user-store

A simple Python REST API server with a thread-safe in-memory user store.

## About 

This project implements a basic REST HTTP API server in Python using only the standard library. It provides a thread-safe in-memory store for user data,
allowing clients to create, read, update, and delete user information via JSON over HTTP.

The server supports standard HTTP methods (GET, POST, PUT, PATCH, DELETE) to perform CRUD operations on user resources. The data is stored in memory
with thread safety ensured by locking, making it safe for use with concurrent requests within a single process.

## Getting Started 
### Requirements

-python 3.6+

No external packages are needed — everything uses the Python standard library.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/daheng414514/thread-safe-user-store.git
```

### How to Run the Server

Once you get the code from the repository and active the python enviroment:
```bush
python server.py
```

Then you should see: 
```bush
Server running on http://127.0.0.1:8000
```

This means your REST API server is now running and ready to accept requests

You can now use tools like curl, Postman, or a browser to interact with the API.

Example:
```bush
curl http://127.0.0.1:8000/users
```

#### Notes

* The server will run on localhost (127.0.0.1)
* It listens on port 8000 by default
* You can open the URL in a browser or send HTTP requests from the terminal

