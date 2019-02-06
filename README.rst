portainer-py
============


.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

portainer-py is distributed on `PyPI <https://pypi.org>`_ as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 3.5+.

.. code-block:: bash

    $ pip install portainer-py

Usage
-----

If you're running Portainer locally, which should be very easy using
Docker, connect to it like this:

.. code-block:: python

    from portainer_py import portainer_for_host

    portainer = portainer_for_host("http://localhost:9000")
    portainer.login("<username>", "<password>")

    stack = portainer.stack_with_name("my-stack")

    try:
        portainer.update_stack(
            stack["Id"],
            "path/to/stackfile.yml",
            env_vars={"foo": "bar"}
        )
    except: PortainerError as error:
        print(error.message)


License
-------

portainer-py is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.
