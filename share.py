import click
from socket_server import DmToolsServer, JsonClient
from campaign_map import launch_map_editor
import queue


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
@click.argument("map_name")
@click.pass_context
def start_server(ctx, map_name):
    """
    Starts a server, controlled by the GM.
    """
    q = queue.Queue()
    c = DmToolsServer(q)
    c.start()
    launch_map_editor(ctx, map_name, queue=q)

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
    c.send({"command": "get"})
    data = c.read()
    print(data.keys())
    launch_map_editor(ctx, data["name"], client=JsonClient)



client.add_command(client_join)

share.add_command(server)
share.add_command(client)
