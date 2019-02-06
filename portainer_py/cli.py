import click
from portainer_py import portainer_for_host, PortainerError


@click.command()
@click.option("--stackfile", help="Path to the stackfile")
@click.option("--host", help="URL to Portainer host", envvar="PORTAINER_HOST")
@click.option("--user", help="Portainer username", envvar="PORTAINER_USERNAME")
@click.option("--password", help="Portainer password", envvar="PORTAINER_PASSWORD")
@click.option("--stackname", help="Name of the Portainer stack", envvar="PORTAINER_STACK_NAME")
@click.option("--env", multiple=True)
@click.option('--prune-env', default=False, is_flag=True)
def deploy(stackfile, host, user, password, stackname, env, prune_env):
    # Log in and find the specified stack:
    portainer = portainer_for_host(host)
    portainer.login(user, password)
    stack = portainer.stack_with_name(stackname)

    # Merge existing env vars on the stack with the supplied ones
    existing_env_vars = {} if prune_env else portainer.get_env_vars(stack["Id"])
    env_vars = {k: v for k, v in (item.split('=', 1) for item in env)}

    try:
        portainer.update_stack_with_file(
            stack["Id"], stackfile, env_vars={**existing_env_vars, **env_vars}
        )
    except PortainerError as err:
        print("ERROR:")
        print(err.message)


if __name__ == "__main__":
    deploy()
