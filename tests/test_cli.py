#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import responses
from click.testing import CliRunner

from portainer_py.cli import cli


@responses.activate
def test_deploy(tmp_path):
    """More of a complete flow test than a unit test."""

    def url(path):
        """Helper function for creating URLs"""
        return "http://test.com/api/{}".format(path)

    # Set up mock response for the calls that will be executed:

    stack_json = {"Id": 99, "Name": "test1", "Env": [{"name": "k1", "value": "v1"}]}

    responses.add("GET", url("status"), json={"Version": "1.17.2"})
    responses.add("POST", url("auth"), json={"jwt": "<token>"})
    responses.add("GET", url("endpoints/1/stacks"), json=[stack_json])
    responses.add("GET", url("stacks/99"), json=stack_json)
    responses.add("PUT", url("stacks/99"), json=stack_json)

    # Create fake Stack file:
    stackfile = tmp_path / "stackfile.yml"
    stackfile.write_text("version: '3.6'\n")

    runner = CliRunner()
    command = (
        "deploy "
        "--user foo "  # Username
        "--password bar "  # Password
        "--host http://test.com "  # Portainer host
        "--stackfile {stackfile} "  # Path to stackfile
        "--stackname test1 "  # Name of the stack
        "--env BAZ=bong "  # explicitly passed env var 
        "DOOWOP "  # pass defined env var
    ).format(stackfile=stackfile)
    result = runner.invoke(cli, command, env={"DOOWOP": "that thing"})

    # We expect these calls:

    # GET on /api/status for the version check
    assert responses.calls[0].request.url == "http://test.com/api/status"

    # POST on /api/auth for logging in
    # Make sure the supplied username and password were used
    assert responses.calls[1].request.url == "http://test.com/api/auth"
    login_response = json.loads(responses.calls[1].request.body.decode("utf-8"))
    assert login_response["Username"] == "foo"
    assert login_response["Password"] == "bar"

    # GET on /api/endpoints/1/stacks for finding the stack
    assert responses.calls[2].request.url == "http://test.com/api/endpoints/1/stacks"

    # GET on /api/endpoints/1/stacks/99 for getting the env vars
    assert responses.calls[3].request.url == "http://test.com/api/stacks/99"

    # PUT on /api/endpoints/1/stacks/99 for updating the stack
    update_call = responses.calls[4]
    assert update_call.request.url == "http://test.com/api/stacks/99"
    assert update_call.request.method == "PUT"
    update_body = json.loads(update_call.request.body.decode("utf-8"))
    assert update_body["StackFileContent"] == "version: '3.6'\n"
    assert update_body["Prune"] == False

    # Make sure the existing env vars are sent with the update...
    assert {"name": "k1", "value": "v1"} in update_body["Env"]

    # ...as well as the new ones we supplied in the CLI call
    assert {"name": "BAZ", "value": "bong"} in update_body["Env"]

    # .. and the passed existing variable
    assert {"name": "DOOWOP", "value": "that thing"} in update_body["Env"]

    assert "Stack successfully updated" in result.output
