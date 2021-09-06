'''                                                     Bot Manager                                                  '''
'''
    This is a fancy file to manage the differences between the two bot sides
    i.e. reformatting code between the two bots, and sending files to discord properly
'''
import hashlib, discord
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputFile
from setupfiles.helpers import simplifyString

class BotMgr:

    def __init__(self,tgbot,clrtext,metg):
        self.clr = clrtext
        self.tgbot = tgbot
        self.metg = metg


    # Alright, we got a WHOLE lot of named variables, but for good reason
    # message, channel distinguish telegram, discord;
    #   and message is used to generate the new message id and channel is used to reply
    # content is text, photo is photo, deckfiles is deck file paths
    async def send(self,content,message=None,channel=None):
        # Unpack content
        # Content will always come in this triple
        text, photo, deckfiles = content
        # Telegram block
        if message:
            await self._toTelegram(message,text,photo)
        # Discord block
        elif channel:
            await self._toDiscord(channel,text,photo,deckfiles)

    ##########################################################################
    ##########################################################################



    # Telegram

    async def _toTelegram(self,message,content,photo):
        query = ' '.join(simplifyString(message.query.split()[1:])) # Then the whole string query
        # get message id hash and set up an empty article container
        newhash = hashlib.md5(message.id.encode()).hexdigest()
        arts = []
        # Same with photo content
        if photo:
            photoart = await self._photoArticle(newhash,photo)
            arts.append(photoart)
        # Turn the text input into a text article that telegrm can handle
        if content:
            textart = self._textArticle(query,newhash,content)
            arts.append(textart)
        # Send whichever is available
        if arts:
            await self.tgbot.answer_inline_query(message.id,results=arts,cache_time=1)

    # Converts text to a telegram text article
    def _textArticle(self,query,newhash,content):
        input_content = InputTextMessageContent(''.join(content))
        textart = InlineQueryResultArticle(
            id=newhash,
            title=f'Information for {query!r}',
            input_message_content=input_content,
        )
        return textart

    async def _photoArticle(self,newhash,photo):
        # That part is specifically to make sure it CAN send the file, cuz if it's too big it wont send
        cardphoto = InputFile(photo)
        # Sends the pic to me, saves the file id, and deletes the photo
        pic = await self.tgbot.send_photo(self.metg, cardphoto)
        await self.tgbot.delete_message(self.metg, pic.message_id)
        # Catches telegram id of photo and turns it into file for me
        photoid = pic.photo[0].file_id
        cardpic = InlineQueryResultCachedPhoto(id=newhash+"1", photo_file_id=photoid)
        return cardpic




    ##########################################################################
    ##########################################################################



    # Discord

    async def _toDiscord(self,channel,content,photo,deckfiles):
        # Photo block
        if photo:
            photof = discord.File(photo)
            await channel.send(file=photof)
        # Text block
        if content:
            textchunks = self._chunkMessage(content)
            for t in textchunks:
               await channel.send(t)
        # Gets deck files as names and discord files
        if deckfiles:
            namedfs = self._getNameDfs(deckfiles)
            for ndf in namedfs:
                await channel.send(f"**{ndf[1]}**") # title name
                await channel.send(file=discord.File(ndf[0], ndf[1])) # text file, title name
                await channel.send(self.clr) #clear spaces


    # Get the names and discord files as tuples
    def _getNameDfs(self,deckfiles):
        namedfs = []
        for f in deckfiles:
            if f == None:
                continue
            namedfs.append((open(f[0],'rb'),f[1]))
        return namedfs


    # Chunkify it in case discord cant handle the LENGTH
    def _chunkMessage(self,data):
        msgmax = 2000
        chunk = [data]
        # If the data is more than 2000 characters,
        if len(data) > msgmax:
            # break it into two
            chunk = [data[:msgmax], data[msgmax:]]
            # Then break it until it's in chunks of 2000 characters
            while len(chunk[-1]) > msgmax:
                chunk = chunk[:-1] + [chunk[-1][:msgmax]] + [chunk[-1][msgmax:]]
        return chunk