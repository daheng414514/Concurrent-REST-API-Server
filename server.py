"""
    HTTP REST API server for user data.

    This module implements a simple HTTP server that uses the thread-safe Store class to manage users via JSON.
    It supports the HTTP methods GET, POST, PUT, PATCH, and DELETE to perform CRUD operations on user data.

    Example:
    GET    /users
    POST   /users
    GET    /users/<name>
    PUT    /users/<name>
    PATCH  /users/<name>
    DELETE /users/<name>
"""


from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from functions import Store
from urllib.parse import unquote
import time

store = Store()

class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        max_length = 1024 * 1024
        if length > max_length:
            raise ValueError("Request body too large")

        raw = self.rfile.read(length)
        try:
            obj = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")

        if not isinstance(obj, dict):
            raise TypeError("JSON body must be an JSON object (e.g. {...})")
        return obj



    def do_GET(self):
        path = self.path.split("?", 1)[0]

        try:
            if path == "/users":
                data = store.list_users()
                self._send_json(200, data)


            # Used to test concurrency.
            # /slow will sleep for 5 seconds.
            # If the server is single-threaded, other requests will be blocked.
            if self.path == "/slow":
                time.sleep(5)
                self._send_json(200, {"msg": "slow done"})



            elif path.startswith("/users/"):
                encoded_name = path[len("/users/"):]
                name = unquote(encoded_name)
                data = store.get_user_info(name)
                self._send_json(200, data)

            else:
                self._send_json(404, {"error": "Not found"})

        except KeyError as e:
            self._send_json(404, {"error": str(e)})

        except Exception:
            self._send_json(500, {"error": "Server error"})



    def do_PUT(self):
        path = self.path.split("?", 1)[0]

        try:
            if not path.startswith("/users/"):
                self._send_json(404, {"error": "Not found"})
                return

            encoded_name = path[len("/users/"):]
            name = unquote(encoded_name)
            if not name:
                self._send_json(400, {"error": "Missing user name in path"})
                return

            obj = self._read_json()
            if obj == {}:
                self._send_json(400, {"error": "User info cannot be empty"})
                return
            if name in obj:
                del obj[name]

            changed_info = store.put_user_info(name, obj)
            self._send_json(200, {"name": name, "info": changed_info})

        except (ValueError, TypeError) as e:
            self._send_json(400, {"error": str(e)})

        except KeyError as e:
            self._send_json(404, {"error": str(e)})

        except Exception:
            self._send_json(500, {"error": "Server error"})



    def do_PATCH(self):
        path = self.path.split("?", 1)[0]

        try:
            if not path.startswith("/users/"):
                self._send_json(404, {"error": "Not found"})
                return

            encoded_name = path[len("/users/"):]
            name = unquote(encoded_name)
            if not name:
                self._send_json(400, {"error": "Missing user name in path"})
                return

            obj = self._read_json()
            if obj == {}:
                self._send_json(400, {"error": "Request body required"})
                return
            if name in obj:
                del obj[name]

            changed_info = store.patch_user_info(name, obj)
            self._send_json(200, {"name": name, "info": changed_info})

        except (ValueError, TypeError) as e:
            self._send_json(400, {"error": str(e)})

        except KeyError as e:
            self._send_json(404, {"error": str(e)})

        except Exception:
            self._send_json(500, {"error": "Server error"})



    def do_POST(self):
        path = self.path.split("?", 1)[0]

        try:
            if path != "/users":
                self._send_json(404, {"error": "Not found"})
                return

            obj = self._read_json()

            if "name" not in obj:
                self._send_json(400, {"error": "Missing required field: name"})
                return

            name = obj["name"]
            if not isinstance(name, str) or not name.strip():
                self._send_json(400, {"error": "Name must be a non-empty string"})
                return

            info = dict(obj)
            del info["name"]
            if not info:
                self._send_json(400, {"error": "User info cannot be empty"})
                return

            new_id = store.post_user_info(name, info)

            self._send_json(201, {"id": new_id, "name": name, "info": info})

        except (ValueError, TypeError) as e:
            self._send_json(400, {"error": str(e)})

        except KeyError as e:
            self._send_json(409, {"error": str(e)})

        except Exception:
            self._send_json(500, {"error": "Server error"})



    def do_DELETE(self):
        path = self.path.split("?", 1)[0]

        try:
            if not path.startswith("/users/"):
                self._send_json(404, {"error": "Not found"})
                return

            encoded_name = path[len("/users/"):]
            name = unquote(encoded_name)

            if not name:
                self._send_json(400, {"error": "Missing user name in path"})
                return

            deleted_info = store.delete_user_info(name)

            self._send_json(200, {"name": name, "deleted": deleted_info})

        except KeyError as e:
            self._send_json(404, {"error": str(e)})

        except Exception:
            self._send_json(500, {"error": "Server error"})
    



      

if __name__ == "__main__":
    host="127.0.0.1"
    port=8000
    httpd = ThreadingHTTPServer((host, port), RequestHandler)
    print(f"Server running on http://{host}:{port}")
    httpd.serve_forever()  



## how to use curl:
## curl -X METHOD "$URL" \      URL="http://127.0.0.1:8000" (local) 
## -H "$HEADER" \       HEADER="Content-Type: application:json"
## -d 'body'