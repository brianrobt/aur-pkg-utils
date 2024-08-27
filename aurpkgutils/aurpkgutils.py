"""Main module for AUR Package Utils."""

import re
from typing import Any, Dict, NamedTuple

import lxml
import requests
from bs4 import BeautifulSoup
from requests.api import get

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


# https://github.com/marcelotduarte/cx_Freeze/releases
def check():
    source_url = _get_source_url_root() + "/releases"
    pkgver = _get_pkgver()
    pkgname = _get_pkgname()
    latest = _check_latest(source_url)
    needs_update = _compare_latest(pkgver, latest)

    if needs_update:
        print(
            pkgname
            + " needs to be updated to "
            + latest
            + ". Current version is "
            + pkgver
            + "."
        )
    else:
        print(pkgname + " is up to date.")

    return needs_update


# https://github.com/marcelotduarte/cx_Freeze/archive/$pkgver/$pkgname-$pkgver.tar.gz
def _build_source_url():
    source_url_raw = _get_source_url_raw()
    pkgver = _get_pkgver()
    pkgname = _get_pkgname()
    source_url = (
        source_url_raw + "/" + pkgver + "/" + pkgname + "-" + pkgver + ".tar.gz"
    )
    print(source_url)
    return source_url


# https://github.com/marcelotduarte/cx_Freeze/releases/tag/7.2.0
# https://github.com/marcelotduarte/cx_Freeze/archive/refs/tags/7.2.0.tar.gz
def _check_latest(url: str):
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
    # print("Latest release version: ", latest_release_version.strip())
    # print("Latest release URL: ", latest_release_url.strip())
    return latest_release_version.strip()


def _compare_latest(pkgver: str, latest: str):
    # pkgver_latest = _check_latest(url)
    # pkgver = _get_pkgver()
    # pkgname = _get_pkgname()
    # if pkgver_latest == pkgver:
    #     print("Packages are the same version.  No need to update.")
    # else:
    #     print("Package has an available update.")
    #     print("Latest version: ", pkgver_latest)
    #     print("Local version: ", pkgver)
    #     print("Package name: ", pkgname)
    #
    if latest > pkgver:
        return True
    else:
        return False


def _get_pkgver():
    with open("PKGBUILD", "r+") as pkgbuild_file:
        for line in pkgbuild_file.readlines():
            if re.search("^pkgver", line, re.I):
                return line.split("=")[1].strip()
    return 'ERROR: Could not find "pkgver" in PKGBUILD.'


# https://github.com/marcelotduarte/cx_Freeze/archive/$pkgver/$pkgname-$pkgver.tar.gz
def _get_pkgname():
    with open("PKGBUILD", "r+") as pkgbuild_file:
        for line in pkgbuild_file.readlines():
            if re.search("^pkgname", line, re.I):
                return line.split("=")[1].strip()
    return 'ERROR: Could not find "pkgname" in PKGBUILD.'


def _get_source_url_root():
    with open("PKGBUILD", "r+") as pkgbuild_file:
        for line in pkgbuild_file.readlines():
            if re.search("^source", line, re.I):
                return "/".join(line.strip().split('"')[1].split("/")[:-3])
    return "ERROR: Could not parse repository source root from PKGBUILD."


def _get_source_url_raw():
    # https://github.com/marcelotduarte/cx_Freeze/releases/
    with open("PKGBUILD", "r+") as pkgbuild_file:
        for line in pkgbuild_file.readlines():
            if re.search("^source", line, re.I):
                # print(line)
                # print("/".join(line.strip().split('"')[1].split("/")[:-2]))
                return "/".join(line.strip().split('"')[1].split("/")[:-2])
    return 'ERROR: Could not parse "source" from PKGBUILD.'
