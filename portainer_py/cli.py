import click
from portainer_py import portainer_for_host, PortainerError


@click.command()
@click.option("--stackfile", help="Path to the stackfile")
@click.option("--host", help="URL to Portainer host", envvar="PORTAINER_HOST")
@click.option("--user", help="Portainer username", envvar="PORTAINER_USERNAME")
@click.option("--password", help="Portainer password", envvar="PORTAINER_PASSWORD")
@click.option("--stackname", help="Name of the Portainer stack", envvar="PORTAINER_STACK_NAME")
def deploy(stackfile, host, user, password, stackname):

    portainer = portainer_for_host(host)
    portainer.login(user, password)

    stack = portainer.stack_with_name(stackname)
    print(f"stack found: Id: {stack['Id']}")


if __name__ == "__main__":
    deploy()
