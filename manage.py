#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
   
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')



    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
