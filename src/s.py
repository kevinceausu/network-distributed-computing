from jsonrpcserver import Success, method, serve
import sys
import os
import requests
from jsonrpcclient import request, parse
import subprocess
import threading

# Get server number from command line
if len(sys.argv) > 1:
    serverNumber = sys.argv[1]
else:
    print("sorry you forgot to add a server number... shutting down")
    quit()

# List of known friend servers
myFriends = []

@method
def ping():
    return Success("pong")

@method
def whoareyou():
    portNumber = "500" + serverNumber
    return Success(f"I am server {serverNumber} running on port {portNumber}")

@method
def get_version():
    return Success(sys.version)

@method
def make_folder(foldername):
    try:
        os.mkdir(foldername)
        return Success(f"Folder '{foldername}' created")
    except FileExistsError:
        return Success("Folder already exists")
    

@method
def delete_folder(foldername):
    try:
        os.rmdir(foldername)
        return Success(f"Folder '{foldername}' deleted")
    except FileNotFoundError:
        return Success("Folder not found")
    except OSError:
        return Success("Folder not empty")
    

@method
def search(filename):
    files = os.listdir(".")
    if filename in files:
        return Success(f"{filename} found")
    else:
        return Success(f"{filename} not found")
    
@method
def list_friends():
    if len(myFriends) == 0:
        return Success("No friends known")
    return Success(", ".join(str(friend) for friend in myFriends))


@method
def online(port):
    port = int(port)

    if port not in myFriends:
        myFriends.append(port)

    # tell other friends this server is online too
    for friend in myFriends:
        if friend != port:
            try:
                requests.post(
                    f"http://localhost:{friend}/",
                    json=request("add_friend", params={"port": port})
                )
            except:
                pass

    return Success(f"Server on port {port} is now online")


@method
def add_friend(port):
    port = int(port)
    if port not in myFriends:
        myFriends.append(port)
    return Success("friend added")

@method
def offline(port):
    port = int(port)

    if port in myFriends:
        myFriends.remove(port)

    for friend in myFriends:
        try:
            requests.post(
                f"http://localhost:{friend}/",
                json=request("remove_friend", params={"port": port})
            )
        except:
            pass

    return Success(f"Server on port {port} is now offline")

@method
def remove_friend(port):
    port = int(port)
    if port in myFriends:
        myFriends.remove(port)
    return Success("friend removed")

@method
def heartbeat():
    if len(myFriends) == 0:
        return Success("No friends to ping")

    results = []

    for friend in myFriends:
        try:
            response = requests.post(
                f"http://localhost:{friend}/",
                json=request("ping")
            )
            parsed = parse(response.json())
            results.append(f"{friend}: {parsed.result}")
        except:
            results.append(f"{friend}: no response")

    return Success(" | ".join(results))


@method
def startup(x):
    x = str(x)
    newPort = int("500" + x)

    try:
        #start another server process
        subprocess.Popen([sys.executable, os.path.abspath(__file__), x])

        # tell this server / network that the new server is online
        if newPort not in myFriends:
            myFriends.append(newPort)

        for friend in myFriends:
            if friend != newPort:
                try:
                    requests.post(
                        f"http://localhost:{friend}/",
                        json=request("add_friend", params={"port": newPort})
                    )
                except:
                    pass

        return Success(f"Started server {x} on port {newPort}")
    except Exception as e:
        return Success(f"Could not start server: {str(e)}")
    


@method
def shutdown(x):
    x = str(x)
    targetPort = int("500" + x)

    # tell all known friends that this target is offline
    if targetPort in myFriends:
        myFriends.remove(targetPort)

    for friend in myFriends:
        try:
            requests.post(
                f"http://localhost:{friend}/",
                json=request("remove_friend", params={"port": targetPort})
            )
        except:
            pass

#tell the target server to shut itself down
    try:
        requests.post(
            f"http://localhost:{targetPort}/",
            json=request("shutdown_self")
        )
        return Success(f"Shutdown signal sent to server {x}")
    except:
        return Success(f"Could not contact server {x} on port {targetPort}")
    

@method
def pass_message(msg, x, visited=None):
    if visited is None:
        visited = []

    targetServer = str(x)
    myPort = int("500" + serverNumber)

    if myPort in visited:
        return Success("Already visited this server")

    visited.append(myPort)

# if this server is the target
    if serverNumber == targetServer:
        return Success(f"Message received by server {serverNumber}: {msg}")

    #otherwise pass to friends
    for friend in myFriends:
        if friend not in visited:
            try:
                response = requests.post(
                    f"http://localhost:{friend}/",
                    json=request(
                        "pass_message",
                        params={"msg": msg, "x": x, "visited": visited}
                    )
                )
                parsed = parse(response.json())
                return Success(parsed.result)
            except:
                pass

    return Success("Target server not found")


@method
def shutdown_self():
    def stop_server():
        os._exit(0)

    threading.Timer(0.5, stop_server).start()
    return Success("Server shutting down")


if __name__ == "__main__":
    print(f"server number {serverNumber} running.....")
    portNumber = "500" + serverNumber
    serve(port=int(portNumber))