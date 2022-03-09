'''                                                     MANABOT                                                      '''
'''
    The one! the only!!! MANABOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOT
'''
from init import *

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Startups

async def startAlert():
    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    upmsg = f"Bot has started: {dt}"
    await tgbot.send_message(metg,upmsg)

async def on_startup(d: Dispatcher):
    asyncio.create_task(startAlert())


@client.event
async def on_ready():
    # Start the telegram bot WITHIN the discord bot; this is how it will run both without one blocking the other
    await on_startup(dp)
    await dp.skip_updates()
    asyncio.ensure_future(dp.start_polling())

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    dt = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Send me uptime log
    user = await client.fetch_user(medc)
    await user.send(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n{dt})')
    asyncio.create_task(managers[0].scheduledClear())
    if sys.argv and "clearhash" in sys.argv:
        print("Clearing hash")
        UpdateManager.clearHash()
    if not sys.argv or "noupdate" not in sys.argv:
        print("Updating database")
        asyncio.create_task(UpdateManager.checkUpdate(managers[1]))
    else:
        print("Skipping database update")

# Telegram

@dp.inline_handler()
async def on_inline(message: InlineQuery):
    tosend = open(tgbothelp).read()

    cmd = simplifyString(message.query.split()[0]) # Since you can search *either* card or rule, we use command
    cmd = '!'+cmd
    query = simplifyString(' '.join(message.query.split()[1:]))
    for mgr in managers:
        if cmd in mgr.cmds:
            tosend = await mgr.handle(cmd,query)

    await BotManager.send(tosend,message=message)

# Discord

@client.event
async def on_message(message):
    channel = message.channel
    content = message.content

    if message.author == client.user:
        return

    contParsed = content.split()


    if len(contParsed):
        cmd = contParsed[0].lower()
        query = simplifyString(' '.join(contParsed[1:]))
        for mgr in managers:
            if cmd in mgr.cmds:
                if message.attachments:
                    msgatt = message.attachments[0]
                    tosend = await managers[0].handle(cmd,query,attached=[msgatt.filename,msgatt.url])
                else:
                    tosend = await mgr.handle(cmd,query)

                await BotManager.send(tosend,channel=channel)

    elif message.attachments:
        msgatt = message.attachments[0]
        tosend = await managers[0].handle('','',attached=[msgatt.filename,msgatt.url])
        await BotManager.send(tosend,channel=channel)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(client.run(DCTOKEN))
    loop.run_forever()