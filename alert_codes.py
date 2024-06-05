from enum import Enum
username = "IEEE Alert"
room = "IEEE"
class AlertCode():
    OPEN = {
        "content": f"Looks like the {room} is open! :sunglasses:",
        "username": username
    }
    CLOSED = {
        "content": f"Looks like the {room} is no longer open :disappointed:",
        "username": username
    }
    TEST = {
        "content": "Results of testing the messaging functionality on discord: ",
        "username": username
    }
    POWERON = {
        "content": "Powering on!",
        "username": username
    }
    POWEROFF = {
        "content": "Time for a graceful shutdown :(",
        "username": username
    }
    INTERP_ERROR = {
        "content": "Looks like we ran into an error and I'm not sure what to send out :(",
        "username": username
    }
    TEST_MESSAGE = {
        "content" : "Results of testing the messaging functionality on discord: ",
        "username" : username
    }
