#!/usr/bin/env python
import os
import sys
import subprocess

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeMarket.settings")
    if len(sys.argv) > 1:
        if sys.argv[1] == "browser":
            subprocess.call(["python", "manage.py", 'test', 'marketapp/tests/tests_selenium'] + sys.argv[2:])
        elif sys.argv[1] == "naobrowser":
            subprocess.call(["python", "manage.py", 'test', '--exclude-dir=marketapp/tests/tests_selenium'] + sys.argv[2:])
        elif sys.argv[1] == "todos":
            subprocess.call(["nosetests"] + sys.argv[2:])
    else:
        print "Voce deve usar algum parametro: browser, naobrowser ou todos"
