import os

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Dev(Common):
    # INSTALLED_APPS = Common.INSTALLED_APPS
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))