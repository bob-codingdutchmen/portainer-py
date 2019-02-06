import click
from portainer_py import portainer_for_host, PortainerError


@click.command()
@click.option("--stackfile", help="Path to the stackfile")
@click.option("--host", help="URL to Portainer host", envvar="PORTAINER_HOST")
@click.option("--user", help="Portainer username", envvar="PORTAINER_USERNAME")
@click.option("--password", help="Portainer password", envvar="PORTAINER_PASSWORD")
@click.option("--stackname", help="Name of the Portainer stack", envvar="PORTAINER_STACK_NAME")
@click.option("--env", nargs=2, type=str, multiple=True)
def deploy(stackfile, host, user, password, stackname, env=None):

    portainer = portainer_for_host(host)
    portainer.login(user, password)

    stack = portainer.stack_with_name(stackname)

    try:
        portainer.update_stack_with_file(
            stack["Id"], stackfile, env_vars={k: v for k, v in env}
        )
    except PortainerError as err:
        print("ERROR:")
        print(err.message)


if __name__ == "__main__":
    deploy()
