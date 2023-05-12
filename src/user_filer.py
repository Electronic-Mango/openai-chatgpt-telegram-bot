from os import getenv

from dotenv import load_dotenv
from telegram.ext.filters import User

load_dotenv()

_usernames = getenv("ALLOWED_USERNAMES", "").split()
user_filter = User(username=_usernames, allow_empty=True)
