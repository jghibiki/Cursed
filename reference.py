import click
import os.path
import shutil
import json
import sys, tempfile, os
import subprocess
try:
    import mdv
except:
    mdv = None

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


@click.group()
def section():
    pass

@click.group()
def article():
    pass


@click.command()
@click.option("--ref-name", default="Reference Name")
@click.option("--overwrite", is_flag=True, default=False)
@click.pass_context
def init(ctx, ref_name, overwrite):
    default_ref = {
        "name": ref_name,
        "sections": []
    }
    ref_exists = os.path.exists(ctx.obj["ref_location"])
    if (ref_exists and overwrite) or not ref_exists:
        save(ctx, default_ref)
        click.echo("Reference file created!")
    elif ref_exists and not overwrite:
        click.echo("Reference file already exists. Use --overwrite to overwrite existing file.")



@click.command()
@click.argument("section_name")
@click.argument("article_name")
@click.option("--markdown", is_flag=True, default=False)
@click.option("--pager", is_flag=True, default=False)
@click.pass_context
def view(ctx, section_name, article_name, markdown, pager):
    ref = load(ctx)

    section_idx = None
    for idx, section in enumerate(ref["sections"]):
        if section["name"] == section_name:
            section_idx = idx
            break

    for article in ref["sections"][section_idx]["articles"]:
        if article["name"] == article_name:
            title = "%s: %s" % (section_name, article_name)
            pad = len(title)*"="

            if markdown and not mdv:
                click.echo("Markdown support is only available if you install the mark down viwer (mdv).\nTry pip install mdv")
            elif markdown and mdv:
                formatted = mdv.main(article["text"], c_theme="readyred", theme="readyred" )


                if not pager:
                    click.echo(formatted)
                else:
                    click.echo_via_pager(formatted)
            else:
                output = "%s\n%s\n%s\n\n" % (pad, title, pad)
                output += article["text"]
                if not pager:
                    click.echo(output)
                else:
                    click.echo_via_pager(output)

@click.command("list")
@click.pass_context
def list(ctx):
    ref = load(ctx)
    intro = "%s" % ref["name"]
    pad = len(intro)*"="
    click.echo("%s\n%s\n%s\nSections" % (pad, intro, pad))
    for idx, section in enumerate(ref["sections"]):
        click.echo("|-> %s: %s" % (idx+1, section["name"]))
        for idx2, article in enumerate(section["articles"]):
            click.echo("||---> %s.%s: %s" % (idx+1, idx2+1, article["name"]))


# Section commands

@click.command("add")
@click.argument("name")
@click.pass_context
def add_section(ctx, name):
    ref = load(ctx)
    for section in ref["sections"]:
        if section["name"] == name:
            exit()

    ref["sections"].append({
        "name": name,
        "articles": []
    })
    save(ctx, ref)

@click.command("rm")
@click.argument("name")
@click.pass_context
def rm_section(ctx, name):
    ref = load(ctx)

    for section in ref["sections"]:
        if section["name"] == name:
            ref["sections"].remove(section)
            save(ctx, ref)
            break

@click.command("rename")
@click.argument("name")
@click.argument("new_name")
@click.pass_context
def rename_section(ctx, name, new_name):
    ref = load(ctx)

    # ensure there is not another one with this name
    if name == new_name: exit()
    count = 0
    for section in ref["sections"]:
        if section["name"] == name:
            count += 1
        if section["name"] == new_name:
            exit()
    if count > 1:
        exit()

    # no existing name to move from/to
    for idx, val in enumerate(ref["sections"]):
        if ref["sections"][idx]["name"] == name:
            ref["sections"][idx]["name"] = new_name
            save(ctx, ref)
            break

@click.command("mv")
@click.argument("name")
@click.option("--up", is_flag=True, default=False)
@click.option("--down", is_flag=True, default=False)
@click.pass_context
def mv_section(ctx, name, up, down):
    ref = load(ctx)

    if (not up and not down) or (up and down):
        click.echo("Must previde either --up or --down")
        exit()

    if up and not down:
        mod = -1
    elif down and not up:
        mod = 1

    for idx, section in enumerate(ref["sections"]):
        if section["name"] == name:
            ref["sections"].remove(section)
            ref["sections"].insert(idx+mod, section)
            save(ctx, ref)
            break



# Article Commands

@click.command("add")
@click.argument("section_name")
@click.argument("name")
@click.pass_context
def add_article(ctx, section_name, name):
    ref = load(ctx)
    section_idx = None
    for idx, section in enumerate(ref["sections"]):
        if section["name"] == section_name:
            section_idx = idx
            break

    if section_idx is not None:
        for article in ref["sections"][section_idx]["articles"]:
            if article["name"] == name:
                exit()

        ref["sections"][section_idx]["articles"].append({
            "name": name,
            "text": ""
        })
        save(ctx, ref)


@click.command("edit")
@click.argument("section_name")
@click.argument("name")
@click.pass_context
def edit_article(ctx, section_name, name):
    ref = load(ctx)

    section_idx = None
    for idx, section in enumerate(ref["sections"]):
        if section["name"] == section_name:
            section_idx = idx
            break

    for article in ref["sections"][section_idx]["articles"]:
        if article["name"] == name:
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                text = article["text"].encode("UTF-8")
                tf.write(text)
                tf.flush()
                subprocess.call([EDITOR, tf.name])

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                article["text"] = tf.read().decode("UTF-8")
            break
    save(ctx, ref)



@click.command("rm")
@click.argument("section_name")
@click.argument("name")
@click.pass_context
def rm_article(ctx, section_name, name):
    ref = load(ctx)

    section_idx = None
    for idx, section in enumerate(ref["sections"]):
        if section["name"] == section_name:
            section_idx = idx
            break

    for article in ref["sections"][section_idx]["articles"]:
        if article["name"] == name:
            ref["sections"][section_idx]["articles"].remove(article)
            save(ctx, ref)
            break

@click.command("rename")
@click.argument("section_name")
@click.argument("name")
@click.argument("new_name")
@click.pass_context
def rename_article(ctx, section_name, name, new_name):
    ref = load(ctx)

    section_idx = None
    for idx, section in enumerate(ref["sections"]):
        if section["name"] == section_name:
            section_idx = idx
            break

    # ensure there is not another one with this name
    if name == new_name: exit()
    count = 0
    for article in ref["sections"][section_idx]["articles"]:
        if article["name"] == name:
            count += 1
        if article["name"] == new_name:
            exit()
    if count > 1:
        exit()

    # no existing name to move from/to
    for idx, val in enumerate(ref["sections"][section_idx]["articles"]):
        if ref["sections"][section_idx]["articles"][idx]["name"] == name:
            ref["sections"][section_idx]["articles"][idx]["name"] = new_name
            save(ctx, ref)
            break

@click.command("mv")
@click.argument("section_name")
@click.argument("name")
@click.option("--up", is_flag=True, default=False)
@click.option("--down", is_flag=True, default=False)
@click.pass_context
def mv_article(ctx, section_name, name, up, down):
    ref = load(ctx)

    if (not up and not down) or (up and down):
        click.echo("Must previde either --up or --down")
        exit()

    section_idx = None
    for idx, section in enumerate(ref["sections"]):
        if section["name"] == section_name:
            section_idx = idx
            break

    if up and not down:
        mod = -1
    elif down and not up:
        mod = 1

    for idx, article in enumerate(ref["sections"][section_idx]["articles"]):
        if article["name"] == name:
            ref["sections"][section_idx]["articles"].remove(article)
            ref["sections"][section_idx]["articles"].insert(idx+mod, article)
            save(ctx, ref)
            break

section.add_command(add_section)
section.add_command(mv_section)
section.add_command(rm_section)
section.add_command(rename_section)

article.add_command(add_article)
article.add_command(mv_article)
article.add_command(edit_article)
article.add_command(rm_article)
article.add_command(rename_article)


ref.add_command(list)
ref.add_command(init)
ref.add_command(view)
ref.add_command(article)
ref.add_command(section)

