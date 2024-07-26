"""Main module for AUR Package Utils."""

import re
from typing import Any, Dict, NamedTuple

import lxml
import requests
from bs4 import BeautifulSoup

# r = requests.get("https://github.com/marcelotduarte/cx_Freeze/releases/")
#
# soup = BeautifulSoup(r.content, "lxml")
#
# s = soup.find("a", class_="Link--primary")
#
# regex = re.compile("\\d+.\\d+.\\d+")
# match = re.search(regex, s.text)
# print(match.group())


def check_latest(url: str):
    repo_raw = requests.get(url)
    repo_soup = BeautifulSoup(repo_raw.content, "lxml")
    latest_release_link = repo_soup.find("a", class_="Link--primary")
    semver_regex = re.compile("\\d+.\\d+.\\d+")
    latest_release_version = re.search(semver_regex, latest_release_link.text)
    print(latest_release_version.group())
