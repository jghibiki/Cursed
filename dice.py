import click
import random

@click.command()
@click.argument("dice")
@click.option("--stats", is_flag=True, default=False)
@click.option("--each", is_flag=True, default=False)
@click.option("--quiet", is_flag=True, default=False)
@click.pass_context
def roll(ctx, dice, stats, each, quiet):
    split = dice.split("d")

    num = int(split[0])
    die = int(split[1])

    if not quiet: print("Rolling %sd%s" %(num, die))

    rolls = []
    cum = 0
    for x in range(num):
        roll = random.randint(1, die)
        rolls.append(roll)
        cum += roll
        if each:
            print("|->Roll %s: %s (Cumulative: %s)" % (x+1, roll, cum))
    if not quiet:
        print("Sum: %s" % cum)
        if stats:
            print("Avg: %s" % (cum/num))
            print("Mode: %s" % (max(set(rolls), key=rolls.count)))
    else:
        print(cum)

