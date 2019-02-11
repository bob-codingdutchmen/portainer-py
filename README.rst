portainer-py
============

.. image:: https://travis-ci.org/bob-codingdutchmen/portainer-py.svg?branch=master
    :target: https://travis-ci.org/bob-codingdutchmen/portainer-py

----


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

From the command line
~~~~~~~~~~~~~~~~~~~~~

The only command currently supported is ``deploy``.
Use the help function to find out how to use it:

.. code-block:: bash

    $ portainerpy deploy --help
    Usage: portainerpy deploy [OPTIONS]

      Update and deploy a portainer stack.

      To ease automation, this utility also support using environment variables
      instead of using these command line options:

      --user       PORTAINER_USERNAME
      --password   PORTAINER_PASSWORD
      --host       PORTAINER_HOST
      --stackname  PORTAINER_STACK_NAME
      --stackfile  PORTAINER_STACKFILE

    Options:
      -f, --stackfile PATH  Path to the stackfile.yml  [required]
      -h, --host TEXT       URL to Portainer host  [required]
      -u, --user TEXT       Portainer username  [required]
      -p, --password TEXT   Portainer password
      -n, --stackname TEXT  Name of the Portainer stack  [required]
      -e, --env TEXT        Environment variables to add to the stack
      --prune-env           If true, will remove existing environment variables
                            from the stack
      --prune-stack         Prune services that are no longer referenced
      --help                Show this message and exit.


From python
~~~~~~~~~~~

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
