from distutils.log import warn
import json
import os

import hikari as hk
import lightbulb as lb
from dotenv import load_dotenv
from termcolor import colored

import embeds

# token loading
load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = "!"

# load and read JSON file
with open("warns.json", "r") as f:
    warns = json.load(f)
    print(colored(warns, "red"))


bot = lb.BotApp(
    TOKEN,
    PREFIX,
    help_class=None,
    default_enabled_guilds=(
        580384337044701185, # test server
        1009416096891289651 # SSIS TE22B
        )
    )


@bot.command
@lb.command("ping", "Testa att botten är online.")
@lb.implements(lb.SlashCommand)
async def ping(ctx: lb.context) -> None:
    await ctx.respond(
        hk.Embed(
            title="Pong!",
            description=":ping_pong:"
            ))

@bot.command
@lb.option("user", "The User", hk.Member, required=True)
@lb.command("warn", "Warna a user.")
@lb.implements(lb.SlashCommand)
async def ping(ctx: lb.context) -> None:
    user = str(ctx.options.user)
    member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
    permissions = lb.utils.permissions_for(member)

    if hk.Permissions.ADMINISTRATOR in permissions:
        await ctx.respond(hk.Embed(
            title="User warned",
            description=
                ":warning: " +
                user +
                " :warning:"
        ))

        #print(isinstance(user, warns))
        if user not in warns:
            warns[user] = 1
        else:
            warns[user] += 1
        with open('warns.json', 'w', encoding='utf-8') as f:
            json.dump(warns, f, sort_keys=True, ensure_ascii=False, indent=4)
        
        await bot.rest.create_message(
            "1026815021952532500", 
            "``` json" +
            json.dumps(warns, sort_keys=True, indent=4) +
            "```"
        )

    else:
        await ctx.respond(embeds.missing_perm)


bot.run(activity=hk.Activity(type=hk.ActivityType.WATCHING, name="1984"))
