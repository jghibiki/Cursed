import click
from socket_server import DmToolsServer, JsonClient


@click.group()
@click.pass_context
def share(ctx):
    pass


@click.group()
@click.pass_context
def server(ctx):
    """
    Tools for starting and running a server.
    """
    pass

@click.command("start")
@click.pass_context
def start_server(ctx):
    """
    Starts a server, controlled by the GM.
    """
    c = DmToolsServer()
    c.start()

server.add_command(start_server)


@click.group()
@click.pass_context
def client(ctx):
    """
    Tools for connecting to a dmtools server as a player.
    """
    pass

@click.command("join")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default="5489")
@click.pass_context
def client_join(ctx, host, port):
    """
    Join a dmtools server.
    """
    c = JsonClient()
    c.connect()
    #call c.read() to get data
    c.send({"msg": "test!"})
    c.send({"type": "command", "command": "kill"})
    c.close() # close for now since we don't do anything yet



client.add_command(client_join)

share.add_command(server)
share.add_command(client)
