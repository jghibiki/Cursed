from utils import load, save
import click
import sys, tempfile, os
from subprocess import call

EDITOR = os.environ.get('EDITOR','vim')

@click.group("story")
@click.pass_context
def campaign(ctx):
    pass

@click.command()
@click.argument("name")
@click.pass_context
def add(ctx, name):
    map_obj = load(ctx)

    for chapter in map_obj["story"]:
        if chapter["name"] == name:
            exit()

    map_obj["story"].append({
        "name": name,
        "text": ""
    })
    save(ctx, map_obj)


@click.command()
@click.argument("name")
@click.pass_context
def edit(ctx, name):
    map_obj = load(ctx)
    for chapter in map_obj["story"]:
        if chapter["name"] == name:
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                text = chapter["text"].encode("UTF-8")
                tf.write(text)
                tf.flush()
                call([EDITOR, tf.name])

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                chapter["text"] = tf.read().decode("UTF-8")
            break
    save(ctx, map_obj)


@click.command()
@click.argument("name")
@click.pass_context
def view(ctx, name):
    map_obj = load(ctx)
    for chapter in map_obj["story"]:
        if chapter["name"] == name:
            print("%s\n%s" % (name, len(name)*"="))
            print(chapter["text"])

@click.command()
@click.argument("name")
@click.pass_context
def rm(ctx, name):
    map_obj = load(ctx)

    for chapter in map_obj["story"]:
        if chapter["name"] == name:
            map_obj["story"].remove(chapter)
            save(ctx, map_obj)
            break

@click.command()
@click.argument("name")
@click.argument("new_name")
@click.pass_context
def rename(ctx, name, new_name):
    map_obj = load(ctx)

    # ensure there is not another one with this name
    if name == new_name: exit()
    count = 0
    for chapter in map_obj["story"]:
        if chapter["name"] == name:
            count += 1
        if chapter["name"] == new_name:
            exit()
    if count > 1:
        exit()

    # no existing name to move from/to
    for idx in enumerate(map_obj["story"]):
        if map_obj[idx]["name"] == name:
            map_obj[idx]["name"] == new_name
            save(ctx, map_obj)
            break

@click.command()
@click.argument("name")
@click.option("--up", is_flag=True, default=False)
@click.option("--down", is_flag=True, default=False)
@click.pass_context
def mv(ctx, name, up, down):
    map_obj = load(ctx)

    if (not up and not down) or (up and down):
        print("Must previde either --up or --down")
        exit()

    if up and not down:
        mod = -1
    elif down and not up:
        mod = 1

    for idx, chapter in enumerate(map_obj["story"]):
        if chapter["name"] == name:
            map_obj["story"].remove(chapter)
            map_obj["story"].insert(idx+mod, chapter)
            save(ctx, map_obj)
            break

@click.command()
@click.pass_context
def list(ctx):
    map_obj = load(ctx)
    intro = "%s" % map_obj["title"]
    pad = len(intro)*"="
    print("%s\n%s\n%s\nChapters" % (pad, intro, pad))
    for idx, chapter in enumerate(map_obj["story"]):
        print("|-> Chapter %s: %s" % (idx+1, chapter["name"]))


campaign.add_command(add)
campaign.add_command(edit)
campaign.add_command(view)
campaign.add_command(list)
campaign.add_command(rm)
campaign.add_command(rename)
campaign.add_command(mv)



