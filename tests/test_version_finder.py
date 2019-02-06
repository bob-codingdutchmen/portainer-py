#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from portainer_py.api_versions import (
    get_closest_api_version,
    Portainer_1_17,
    Portainer_1_18,
)


class TestVersionFinder:
    @pytest.mark.parametrize(
        "version,portainer_class",
        [
            ("0.0", Portainer_1_17),
            ("1.0", Portainer_1_17),
            ("1.0.999", Portainer_1_17),
            ("1.17", Portainer_1_17),
            ("1.17.1", Portainer_1_17),
            ("1.17.999", Portainer_1_17),
            ("1.18", Portainer_1_18),
            ("1.18.0", Portainer_1_18),
            ("1.18.999", Portainer_1_18),
            ("1.299", Portainer_1_18),
            ("2.000", Portainer_1_18),
            ("10.0.1", Portainer_1_18),
        ],
    )
    def test_version_low(self, version, portainer_class):
        assert get_closest_api_version(version) == portainer_class
