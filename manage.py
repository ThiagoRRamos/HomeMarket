#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeMarket.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

#Fazendo um teste com c9