# -*- coding: utf-8 -*-

"""Main module."""

from urllib.parse import urljoin
from .api_versions import Portainer
import requests

from . import api_versions


def portainer_for_host(host) -> Portainer:
    """
    Finds and returns the right Portainer class for the version
    running on this host
    """
    url = urljoin(host, "api/status")
    r = requests.request("GET", url).json()
    return api_versions.get_closest_api_version(r.get("Version"))(host)
