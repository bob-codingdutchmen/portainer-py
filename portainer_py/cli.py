import os
from typing import Union

import click
from click import option
from colorama import init as colorama_init

from portainer_py import __version__, portainer_for_host, PortainerError

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    colorama_init()


def show_error(message: Union[str, Exception], stop: bool = False):
    click.secho("⨉ Error: {}".format(message), fg="red")
    if stop:
        print()
        exit(1)


@cli.command()
@option(
    "-f",
    "--stackfile",
    help="Path to the stackfile.yml",
    envvar="PORTAINER_STACKFILE",
    type=click.Path(exists=True),
    required=True,
)
@option(
    "-h", "--host", help="URL to Portainer host", envvar="PORTAINER_HOST", required=True
)
@option(
    "-u",
    "--user",
    help="Portainer username",
    envvar="PORTAINER_USERNAME",
    required=True,
)
@option(
    "-p",
    "--password",
    help="Portainer password",
    envvar="PORTAINER_PASSWORD",
    prompt="Portainer password",
    hide_input=True,
)
@option(
    "-n",
    "--stackname",
    help="Name of the Portainer stack",
    envvar="PORTAINER_STACK_NAME",
    required=True,
)
@option("-e", "--env", help="Environment variables to add to the stack", multiple=True)
@option(
    "--prune-env",
    help="If true, will remove existing environment variables from the stack",
    default=False,
    is_flag=True,
)
@option(
    "--prune-stack",
    help="Prune services that are no longer referenced",
    default=False,
    is_flag=True,
)
@click.argument("PASS_ENV_VARS", nargs=-1)
def deploy(
    stackfile,
    host,
    user,
    password,
    stackname,
    env,
    prune_env,
    prune_stack,
    pass_env_vars,
):
    """
    Update and deploy a portainer stack.

    To ease automation, this utility also support using environment variables
    instead of using these command line options:

    \b
    --user       PORTAINER_USERNAME
    --password   PORTAINER_PASSWORD
    --host       PORTAINER_HOST
    --stackname  PORTAINER_STACK_NAME
    --stackfile  PORTAINER_STACKFILE

    Use [PASS_ENV_VARS] to pass the names of the environment variables you want to
    pass on to the Portainer stack
    """

    click.echo("Deploying to portainer @ {host} as {user}".format(host=host, user=user))
    try:
        portainer = portainer_for_host(host)
    except ConnectionError as err:
        show_error(str(err), stop=True)

    try:
        portainer.login(user, password)
    except PortainerError as err:
        show_error(err.message, stop=True)

    try:
        stack = portainer.stack_with_name(stackname)
    except LookupError as err:
        show_error(err, stop=True)

    # Merge existing env vars on the stack with the supplied ones
    env_vars = {} if prune_env else portainer.get_env_vars(stack["Id"])
    env_vars.update({k: v for k, v in (item.split("=", 1) for item in env)})
    env_vars.update({k: os.environ.get(k) for k in pass_env_vars})

    try:
        portainer.update_stack_with_file(
            stack["Id"], stackfile, env_vars=env_vars, prune=prune_stack
        )
    except PortainerError as err:
        show_error(err.message, stop=True)
    except FileNotFoundError as err:
        show_error(err, stop=True)

    click.secho("√ Stack successfully updated!", fg="green")
    print()


if __name__ == "__main__":
    cli()
