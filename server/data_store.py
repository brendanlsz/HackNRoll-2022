from collections import defaultdict
import json
import os.path
from typing import List

STORE = f"{os.path.dirname(os.path.abspath(__file__))}/store.json"


def read_data() -> defaultdict:
    """Returns content of store.json in a dict

    Returns:
        defaultdict: Content of store.json
    """

    data = defaultdict(lambda: {"subscribers": [], "info": ""})
    with open(STORE, "r") as f:
        data = defaultdict(lambda: {
            "subscribers": [], "info": ""
        }, json.loads(f.read()))
        f.close()
    return data


def write_data(data: defaultdict):
    """Overwrites content of store.json

    Args:
        data (defaultdict): The new content of store.json
    """

    with open(STORE, "w") as f:
        json.dump(data, f)
        f.close()


def add_learning_state(learn_id: str, info: str = ""):
    """Adds a new learning session into store.json

    Args:
        learn_id (str): ID generated by the socket server
        info (str, optional): Information you want the user to see from the telegram bot. Defaults to "".
    """
    data = read_data()
    data[learn_id]["info"] = info
    write_data(data)


def del_learning_state(learn_id: str):
    """Removes a learning session from store.json

    Args:
        learn_id (str): ID to be removed
    """
    data = read_data()
    del data[learn_id]
    write_data(data)


def get_learning_state(learn_id: str) -> str:
    """Returns the information to be shown on telegram

    Args:
        learn_id (str): ID generated by the socket server

    Returns:
        str: Information to be shown
    """

    data = read_data()
    return data[learn_id]["info"]


def update_learning_state(learn_id: str, info: str = ""):
    """Updates the information on store.json

    Args:
        learn_id (str): ID generated by the socket server
        info (str, optional): Information to be shown on telegram. Defaults to "".
    """

    data = read_data()
    data[learn_id]["info"] = info
    write_data(data)


def get_subscribers(learn_id: str) -> List[str]:
    """Retrieves list of subscribed chat_ids for learning session

    Args:
        learn_id (str): ID generated by the socket server

    Returns:
        List[str]: List of chat_ids subscribed to learning session
    """

    data = read_data()

    if learn_id in data:
        return data[learn_id]["subscribers"]


def add_subscriber(learn_id: str, username: str) -> str:
    """Adds a telegram user to actively retrieve training updates

    Args:
        learn_id (str): ID generated by the socket server
        username (str): Telegram username

    Returns:
        str: Message of outcome to be relayed to the user
    """

    data = read_data()

    if not learn_id in data:
        return f"id: {learn_id} doesn't exist"
    if username in data[learn_id]["subscribers"]:
        return f"User is already subscribed to id: {learn_id}!"

    data[learn_id]["subscribers"].append(username)
    write_data(data)
    return f"User is now subscribed to id: {learn_id}"


def del_subscriber(learn_id: str, username: str) -> str:
    """Removes telegram user from actively retrieve training updates

    Args:
        learn_id (str): ID generated by the socket server
        username (str): Telegram username

    Returns:
        str: Message of outcome to be relayed to the user
    """

    data = read_data()

    if not learn_id in data:
        return f"id: {learn_id} doesn't exist"
    if username in data[learn_id]["subscribers"]:
        data[learn_id]["subscribers"].remove(username)
        write_data(data)
        return f"User is now unsubscribed from id: {learn_id}"
    else:
        return f"User is not subscribed to id: {learn_id}"