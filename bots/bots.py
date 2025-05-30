import sys, inspect
from modules.bot import Bot

from bots.super_bot import SuperBot


def is_bot_registered(bot_name: str) -> bool:
    class_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for item in class_members:
        if item[0] == bot_name:
            return True
    return False


def get_bot_class_with_name(bot_name: str) -> Bot:
    class_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for item in class_members:
        if item[0] == bot_name:
            return item[1]
    return Bot