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

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/thread-safe-user-store.git
