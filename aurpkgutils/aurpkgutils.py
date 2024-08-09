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


# class AurPkgUtils(NamedTuple):
#     pkgutil: str
#     error: int


GITHUB_BASE = "https://github.com/"


# https://github.com/marcelotduarte/cx_Freeze/releases/tag/7.2.0
# https://github.com/marcelotduarte/cx_Freeze/archive/refs/tags/7.2.0.tar.gz
def check_latest(url: str):
    repo_raw = requests.get(url)
    repo_soup = BeautifulSoup(repo_raw.content, "lxml")
    latest_release_link = repo_soup.find("a", class_="Link--primary")
    latest_release_link_arr = latest_release_link.attrs["href"].split("/")
    github_remote_base_user = latest_release_link_arr[1] + "/"
    github_remote_base_project = latest_release_link_arr[2] + "/"
    semver_regex = re.compile("\\d+.\\d+.\\d+")
    latest_release_version = re.search(semver_regex, latest_release_link.text).group()
    latest_release_url = (
        GITHUB_BASE
        + github_remote_base_user
        + github_remote_base_project
        + "archive/refs/tags/"
        + str(latest_release_version)
        + ".tar.gz"
    )
    print(latest_release_link)
    print(GITHUB_BASE + latest_release_link.attrs["href"])
    print(latest_release_version)
    print(latest_release_url)
