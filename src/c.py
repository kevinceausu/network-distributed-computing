from jsonrpcclient import request, parse, Ok
import requests

def call_ping():
    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("ping")
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")

def call_whoareyou():
    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("whoareyou")
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")

def call_get_version():
    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("get_version")
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")

def call_make_folder():
    print("what folder name?")
    foldername = input()

    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("make_folder", params={"foldername": foldername})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")

def call_delete_folder():
    print("what folder name?")
    foldername = input()

    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("delete_folder", params={"foldername": foldername})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")

def call_search():
    print("what filename to search?")
    filename = input()

    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("search", params={"filename": filename})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")


def call_list_friends():
    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("list_friends")
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")


def call_online():
    print("which server port is coming online?")
    onlinePort = int(input())

    print("send this command to which server?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("online", params={"port": onlinePort})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")


def call_offline():
    print("which server port is going offline?")
    offlinePort = int(input())

    print("send this command to which server?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("offline", params={"port": offlinePort})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")


def call_heartbeat():
    print("what is the servers port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("heartbeat")
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")


def call_startup():
    print("which server number should be started?")
    x = input()

    print("send this command to which server?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("startup", params={"x": x})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")



def call_shutdown():
    print("which server number should be shut down?")
    x = input()

    print("send this command to which server port?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("shutdown", params={"x": x})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")



def call_pass_message():
    print("what message do you want to send?")
    msg = input()

    print("which server number is the target?")
    x = input()

    print("send this command to which server port first?")
    portToCall = int(input())

    try:
        response = requests.post(
            f"http://localhost:{portToCall}/",
            json=request("pass_message", params={"msg": msg, "x": x})
        )
        parsed = parse(response.json())
        print(parsed.result)
    except:
        print("Are you sure that port and function exist?")



print("Welcome!")

while True:
    print("\nplease type a menu option")
    print("1. ping")
    print("2. whoareyou")
    print("3. get_version")
    print("4. make_folder")
    print("5. delete_folder")
    print("6. search")
    print("7. list_friends")
    print("8. online")
    print("9. offline")
    print("10. heartbeat")
    print("11. startup")
    print("12. shutdown")
    print("13. pass message")
    print("14. quit")

    option = int(input())

    if option == 1:
        call_ping()
    elif option == 2:
        call_whoareyou()
    elif option == 3:
        call_get_version()
    elif option == 4:
        call_make_folder()

    elif option == 5:
        call_delete_folder()

    elif option == 6:
        call_search()

    elif option == 7:
        call_list_friends()
    elif option == 8:
        call_online()
    elif option == 9:
        call_offline()
    elif option == 10:
        call_heartbeat()
    elif option == 11:
        call_startup()
    elif option == 12:
        call_shutdown()
    elif option == 13:
        call_pass_message()
    elif option == 14:
         break