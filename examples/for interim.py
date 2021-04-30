import asyncio
import requests

from octii import Message
from octii.bot import Bot, Context

with open("./token.txt") as f:
    bot = Bot(f.readlines()[0], "!")

bot.selfbot = True

@bot.command(name="test")
async def test(ctx: Context):
    """A simple test command. Does nothing."""
    ctx.send("Test command was called!")

@bot.command(name="purge", aliases=["massdel", "massdelete"])
async def purge(ctx: Context, amt: int):
    """Deletes an amount of messages"""
    # Do nothing if another user runs the command, as they may be running the bot on their own account
    if ctx.msg.author_id != bot._api_client.user_id:
        return

    all_msgs = ctx._bot._api_client.get_messages(ctx.channel_id)
    ctx._bot._api_client.delete_message(ctx.msg.id)

    for reply in list(filter(lambda reply: reply.author_id == ctx._bot._api_client.user_id and reply.id != ctx.msg.id, all_msgs))[:amt]:
        ctx._bot._api_client.delete_message(reply.id)

    reply = ctx.send("Successfully purged " + str(amt) + " messages")
    await asyncio.sleep(3)
    ctx._bot._api_client.delete_message(reply.id)

@bot.command(name="reply", aliases=["respond", "quote"])
async def reply(ctx: Context, message: Message):
    """Quotes a message"""
    # Do nothing if another user runs the command, as they may be running the bot on their own account
    if ctx.msg.author_id != bot._api_client.user_id:
        return

    reply_message = "\n".join(map(lambda line: "> " + line, message.content.split("\n")))
    reply_message += "\n\u00A0- <@" + message.author_id + ">\n"

    try:
        reply_message += " ".join(ctx.msg.content.split(" ")[2:])
    except:
        pass

    ctx.send(reply_message)
    ctx._bot._api_client.delete_message(ctx.msg.id)

@bot.command(name="dog", aliases=["woof", "randomdog"])
async def dog(ctx: Context):
    """Gets a random picture of a dog and sends it in the channel the command was called in"""
    image_url = requests.get("https://dog.ceo/api/breeds/image/random").json()['message']
    ctx.send("https://innstor.innatical.com/" + ctx._bot._api_client.upload_file(image_url.split("/")[-1], requests.get(image_url).content))

@bot.command(name="cat", aliases=["meow", "randomcat"])
async def cat(ctx: Context):
    """Gets a random picture of a cat and sends it in the channel the command was called in"""
    image_url = requests.get("https://api.thecatapi.com/v1/images/search?size=full").json()[0]['url']
    ctx.send("https://innstor.innatical.com/" + ctx._bot._api_client.upload_file(image_url.split("/")[-1], requests.get(image_url).content))

# https://api.thecatapi.com/v1/images/search?size=full
# File message is actually just a link to an innstor url

print("I am:", bot._api_client.fetch_user(bot._api_client.user_id))
print("I am in communities:", bot._api_client.get_communities(bot._api_client.user_id))

bot.run()