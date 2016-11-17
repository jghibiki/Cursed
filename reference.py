import click
import os.path
import json
import sys, tempfile, os
from subprocess import call

EDITOR = os.environ.get('EDITOR','vim')

def load(ctx):
    with open(ctx.obj["ref_location"], "r") as f:
        return json.load(f)

def save(ctx, ref):
    with open(ctx.obj["ref_location"], "w") as f:
        json.dump(ref, f, indent=4)

@click.group()
@click.option("--ref-location", default="reference.json")
@click.pass_context
def ref(ctx, ref_location):
    ctx.obj["ref_location"] = ref_location

@click.command()
@click.option("--ref-name", default="Reference Name")
@click.option("--overwrite", is_flag=True, default=False)
@click.pass_context
def init(ctx, ref_name, overwrite):
    default_ref = {
        "name": ref_name,
        "articles": []
    }
    ref_exists = os.path.exists(ctx.obj["ref_location"])
    if (ref_exists and overwrite) or not ref_exists:
        save(ctx, default_ref)
        print("Reference file created!")
    elif ref_exists and not overwrite:
        print("Reference file already exists. Use --overwrite to overwrite existing file.")

@click.command()
@click.argument("name")
@click.pass_context
def add(ctx, name):
    ref = load(ctx)
    for article in ref["articles"]:
        if article["name"] == name:
            exit()

    ref["articles"].append({
        "name": name,
        "text": ""
    })
    save(ctx, ref)


@click.command()
@click.pass_context
def list(ctx):
    ref = load(ctx)
    intro = "%s" % ref["name"]
    pad = len(intro)*"="
    print("%s\n%s\n%s\nArticle" % (pad, intro, pad))
    for idx, article in enumerate(ref["articles"]):
        print("|-> %s: %s" % (idx+1, article["name"]))


@click.command()
@click.argument("name")
@click.pass_context
def edit(ctx, name):
    ref = load(ctx)
    for article in ref["articles"]:
        if article["name"] == name:
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                text = article["text"].encode("UTF-8")
                tf.write(text)
                tf.flush()
                call([EDITOR, tf.name])

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                article["text"] = tf.read().decode("UTF-8")
            break
    save(ctx, ref)


@click.command()
@click.argument("name")
@click.pass_context
def view(ctx, name):
    ref = load(ctx)
    for article in ref["articles"]:
        if article["name"] == name:
            print("%s\n%s" % (name, len(name)*"="))
            print(article["text"])

@click.command()
@click.argument("name")
@click.pass_context
def rm(ctx, name):
    ref = load(ctx)

    for article in ref["articles"]:
        if article["name"] == name:
            ref["articles"].remove(article)
            save(ctx, ref)
            break

@click.command()
@click.argument("name")
@click.argument("new_name")
@click.pass_context
def rename(ctx, name, new_name):
    ref = load(ctx)

    # ensure there is not another one with this name
    if name == new_name: exit()
    count = 0
    for article in ref["articles"]:
        if article["name"] == name:
            count += 1
        if article["name"] == new_name:
            exit()
    if count > 1:
        exit()

    # no existing name to move from/to
    for idx in enumerate(ref["articles"]):
        if map_obj[idx]["name"] == name:
            map_obj[idx]["name"] == new_name
            save(ctx, map_obj)
            break

@click.command()
@click.argument("name")
@click.argument("new_name")
@click.pass_context
def rename(ctx, name, new_name):
    ref = load(ctx)

    # ensure there is not another one with this name
    if name == new_name: exit()
    count = 0
    for article in ref["articles"]:
        if article["name"] == name:
            count += 1
        if article["name"] == new_name:
            exit()
    if count > 1:
        exit()

    # no existing name to move from/to
    for idx, val in enumerate(ref["articles"]):
        if ref["articles"][idx]["name"] == name:
            ref["articles"][idx]["name"] = new_name
            save(ctx, ref)
            break

ref.add_command(init)
ref.add_command(add)
ref.add_command(edit)
ref.add_command(list)
ref.add_command(view)
ref.add_command(rm)
ref.add_command(rename)
