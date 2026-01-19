# thread-safe-user-store

A simple Python REST API server with a thread-safe in-memory user store.

## About 

This project implements a basic REST HTTP API server in Python using only the standard library. 
It provides a thread-safe in-memory store for user data, allowing clients to create, read, update, 
and delete user information via JSON over HTTP.

The server supports standard HTTP methods (GET, POST, PUT, PATCH, DELETE) to perform CRUD operations 
on user resources. The data is stored in memory with thread safety ensured by locking, making it safe 
for use with concurrent requests within a single process.


## Getting Started 
### Requirements

-Python 3.6+

No external packages are needed — everything uses the Python standard library.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/daheng414514/thread-safe-user-store.git
```

### How to Run the Server

Once you clone the repository and activate your Python environment:
```bash
python server.py
```

Then you should see: 
```bash
Server running on http://127.0.0.1:8000
```

This means your REST API server is now running and ready to accept requests

You can now use tools like curl, Postman, or a browser to interact with the API.

Example:
```bash
curl http://127.0.0.1:8000/users
```

#### Notes

* The server will run on localhost (127.0.0.1)
* It listens on port 8000 by default
* You can open the URL in a browser or send HTTP requests from the terminal


## Project Structure

- `server.py` — HTTP server and request handlers
- `functions.py` — Thread-safe in-memory user store
- `test.py` — Unit tests for the store logic


## API Endpoints

The following endpoints are available in this REST API. All requests and responses use JSON.

---

### GET /users

Retrieve a list of all user names.

**Request:**
```bash
curl http://127.0.0.1:8000/users
```

---

### GET /users/<name>

Retrieve info for a specific user.

**Request example:**
```bash
curl "http://127.0.0.1:8000/users/<name>"
```

---

### POST /users

Create a new user by sending JSON in the request body.

**Request example:**
```bash
curl -X POST "http://127.0.0.1:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name":"charlie","age":29,"email":"charlie@example.com"}'
```

---

### PUT /users/<name>

Replace all information for an existing user.

**Request example:**
```bash
curl -X PUT "http://127.0.0.1:8000/users/<name>" \
     -H "Content-Type: application/json" \
     -d '{"age":29,"email":"charlie@example.com"}'
```

---

### PATCH /users/<name>

Update part of an existing user's information by sending JSON in the request body.

**Request example:**
```bash
curl -X PATCH "http://127.0.0.1:8000/users/<name>" \
     -H "Content-Type: application/json" \
     -d '{"age":29,"email":"charlie@example.com"}'
```

---

### DELETE /users/<name>

Delete an existing user by specifying the user name in the URL.

**Request example:**
```bash
curl -X DELETE "http://127.0.0.1:8000/users/<name>"
```

## Notes and Limitations

### Notes
* The server will run on localhost (`127.0.0.1`)
* It listens on port `8000` by default
* You can interact with it using a browser, `curl`, or Postman

### Limitations
* Data is stored in memory and will reset when the server restarts
* Designed for single-process concurrency
* No authentication or persistence layer
* Intended for learning and demonstration purposes


## Testing

The API can be tested using command-line tools such as `curl` or API clients like Postman.

Example commands:

```bash
# Get all user in user database
curl http://127.0.0.1:8000/users

# Create a new user
curl -X POST http://127.0.0.1:8000/users \
     -H "Content-Type: application/json" \
     -d '{"name":"alice","age":30}'

# Update a user
curl -X PATCH http://127.0.0.1:8000/users/alice \
     -H "Content-Type: application/json" \
     -d '{"age":31}'

# Delete a user
curl -X DELETE http://127.0.0.1:8000/users/alice
```
