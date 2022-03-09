'''                                                     Bot Manager                                                  '''
'''
    This is a fancy file to manage the differences between the two bot sides
    i.e. reformatting code between the two bots, and sending files to discord properly
'''
import hashlib, discord
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultCachedPhoto, InputFile
from helpers.helperfns import simplifyString

class BotMgr:

    def __init__(self,tgbot,clrtext,metg):
        self.clr = clrtext
        self.tgbot = tgbot
        self.metg = metg


    async def send(self,content,message=None,channel=None):
        # Content will always come in this triple
        text, photo, deckfiles = content
        if message:
            await self._toTelegram(message,text,photo)
        elif channel:
            await self._toDiscord(channel,text,photo,deckfiles)

    ##########################################################################
    ##########################################################################

    # Telegram

    async def _toTelegram(self,message,content,photo):
        query = ' '.join(message.query.split()[1:])
        # messages require unique hashs, so we're making a new one
        newhash = hashlib.md5(message.id.encode()).hexdigest()
        arts = []
        if photo:
            photoart = await self._photoArticle(newhash,photo)
            arts.append(photoart)
        if content:
            textart = self._textArticle(query,newhash,content)
            arts.append(textart)
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
        cardphoto = InputFile(photo)
        # Sends the pic to me, saves the file id, and deletes the photo
        # This is because telegram can reference pre-uploaded media faster than it can upload new media
        # so if I save the uploaded media's internal file ID, if the same photo gets requested multiple times it will
        # send faster
        pic = await self.tgbot.send_photo(self.metg, cardphoto)
        await self.tgbot.delete_message(self.metg, pic.message_id)
        photoid = pic.photo[0].file_id
        cardpic = InlineQueryResultCachedPhoto(id=newhash+"1", photo_file_id=photoid)
        return cardpic

    ##########################################################################
    ##########################################################################

    # Discord

    async def _toDiscord(self,channel,content,photo,deckfiles):
        if photo:
            photof = discord.File(photo)
            await channel.send(file=photof)
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
                await channel.send(self.clr)

    def _getNameDfs(self,deckfiles):
        namedfs = []
        for f in deckfiles:
            if f == None:
                continue
            namedfs.append((open(f[0],'rb'),f[1]))
        return namedfs

    # Chunkify it in case discord cant handle the LENGTH
    # Cuz discord cant handle text blocks more than 2000 characters
    def _chunkMessage(self,data):
        msgmax = 2000
        chunk = [data]
        if len(data) > msgmax:
            chunk = [data[:msgmax], data[msgmax:]]
            # Repeat the process until the longest message is 2000 or less
            while len(chunk[-1]) > msgmax:
                chunk = chunk[:-1] + [chunk[-1][:msgmax]] + [chunk[-1][msgmax:]]
        return chunk
