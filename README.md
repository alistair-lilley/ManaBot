# ManaBot

Mana bot is a personal project I've developed to use with my friends on Telegram and Discord.

The bot has multiple functionalities, including searching a local database for MTG card images
and rule texts, searching a local database for game rules, rolling dice (RNG based on parsed
rolling descriptors), converting .cod (aka .xml) files to .txt files for easier importing of 
decks, and checking deck lists against ban lists.

The bot runs both on Telegram through the @LF_Mana_Bot *rule/card* `rulename/cardname` command 
and on Discord via the @ManaBot#3013 account.

##Current functionality

Discord:
1. *!card* `cardname`; searches for a card's image and text and posts it
2. *!rule* `keyword/number`; searches for a rule based on a keyword (e.g. Flying) or number
   (e.g. 702.9)
3. *!roll* `XdY[dk/lh]Z+N`; rolls dice in the given format
4. **attachment** *(.cod, .txt) + !checkban*; checks the attached deck against the EDH ban lists for single and
 multiplayer games
5. **attachment** *(.cod, .txt)*; converts file to .txt
6. *!help*; returns the help message

Telegram:
1. *card* `cardname`; searches for a card's image and text and posts it
2. *!rule* `keyword/number`; searches for a rule based on a keyword (e.g. Flying) or number
   (e.g. 702.9)

The bot is continuing to be improved.
