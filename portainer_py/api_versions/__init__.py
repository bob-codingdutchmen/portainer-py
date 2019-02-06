from .portainer_base import Portainer
from .portainer_1_17 import Portainer_1_17
from .portainer_1_18 import Portainer_1_18


def get_closest_api_version(version_string):
    """
    Gets latest API version that matches the version string.
    Any new versions should be added to `all_versions` at the top.
    """
    all_versions = (
        Portainer_1_18,
        Portainer_1_17,
    )
    version = [int(i) for i in version_string.split('.')][:2]

    for portainer in all_versions:
        from_version = getattr(portainer, 'FROM_VERSION')
        if from_version[0] < version[0]:
            return portainer
        elif from_version[0] == version[0] and from_version[1] <= version[1]:
            return portainer

    # No suitable version found!
    return None
