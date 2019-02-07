from typing import Union

import click
from click import option
from colorama import init as colorama_init

from portainer_py import portainer_for_host, PortainerError

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
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
@option("-e", "--env", multiple=True)
@option("--prune-env", default=False, is_flag=True)
@option("--prune-stack", default=False, is_flag=True)
def deploy(stackfile, host, user, password, stackname, env, prune_env, prune_stack):
    """
    Update and deploy a portainer stack.
    """

    portainer = portainer_for_host(host)

    try:
        portainer.login(user, password)
    except PortainerError as err:
        show_error(err.message, stop=True)

    try:
        stack = portainer.stack_with_name(stackname)
    except LookupError as err:
        show_error(err, stop=True)

    # Merge existing env vars on the stack with the supplied ones
    existing_env_vars = {} if prune_env else portainer.get_env_vars(stack["Id"])
    env_vars = {k: v for k, v in (item.split("=", 1) for item in env)}

    try:
        portainer.update_stack_with_file(
            stack["Id"],
            stackfile,
            env_vars={**existing_env_vars, **env_vars},
            prune=prune_stack,
        )
    except PortainerError as err:
        show_error(err.message, stop=True)
    except FileNotFoundError as err:
        show_error(err, stop=True)

    click.secho("√ Stack successfully updated!", fg="green")
    print()


if __name__ == "__main__":
    cli()
