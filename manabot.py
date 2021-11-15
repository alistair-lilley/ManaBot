
'''                                                     MANABOT                                                      '''

'''
    The one! the only!!! MANABOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOT
'''

from init import *

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Startups

# Send startup message
async def startAlert():
    dt = datetime.now().strftime("%d-%m-%Y %H:%M")
    upmsg = f"Bot has started: {dt}"
    await tgbot.send_message(metg,upmsg)

# Startup
async def on_startup(d: Dispatcher):
    asyncio.create_task(startAlert())


# Connect to server
@client.event
async def on_ready():
    # Start the telegram bot WITHIN the discord bot
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

    dt = datetime.now().strftime("%d-%m-%Y %H:%M") # get online time

    # Send me uptime log
    user = await client.fetch_user(medc)
    await user.send(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})\n{dt})')
    asyncio.create_task(managers[0].scheduledClear())
    asyncio.create_task(UpdateManager.checkUpdate())

########################################################################################################################
########################################################################################################################
########################################################################################################################

# TELEGRAM

# Inline handler
# This was one hell of a mess, so lets clean it up!
@dp.inline_handler()
async def on_inline(message: InlineQuery):
    tosend = open(tgbothelp).read()

    # get commands and queries
    cmd = simplifyString(message.query.split()[0]) # Since you can search *either* card or rule, we use command
    cmd = '!'+cmd
    query = ' '.join(simplifyString(message.query.split()[1:])) # Then the whole string query
    for mgr in managers:
        if cmd in mgr.cmds:
            tosend = await mgr.handle(cmd,query)

    await BotManager.send(tosend,message=message)


########################################################################################################################
########################################################################################################################
########################################################################################################################

# DISCORD

# React to messages
@client.event
async def on_message(message):
    # get channel and content data
    channel = message.channel
    content = message.content

    # don't reply to self
    if message.author == client.user:
        return

    # parse content of message
    contParsed = content.split()
    # Get the command


    # if it's a command
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
    loop = asyncio.get_event_loop() # Make an event loop
    loop.create_task(client.run(DCTOKEN)) # Add the discord client
    loop.run_forever() # Run forever