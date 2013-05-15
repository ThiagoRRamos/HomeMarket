#!/usr/bin/env python
import os
import sys
import subprocess

dependencias = ["django",
                "nose-exclude",
                "selenium",
                "nose",
                "django-nose",
                "requests",
                "django-allauth",
                "haystack",
                "pyelasticsearch"]

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HomeMarket.settings")
    if len(sys.argv) > 1:
        if sys.argv[1] == "instalar":
            for dep in dependencias:
                subprocess.call(["pip", "install", dep])
    else:
        for dep in dependencias:
                subprocess.call(["pip", "install", dep])
