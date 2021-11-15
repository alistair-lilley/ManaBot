# ManaBot

---

## Bot Overview

Mana bot is a personal project I've developed to use with my friends on Telegram and Discord.

The bot has multiple functionalities, including searching a local database for MTG card images
and rule texts, searching a local database for game rules, rolling dice (RNG based on parsed
rolling descriptors), converting .cod (aka .xml) files to .txt files for easier importing of 
decks, and checking deck lists against ban lists.

The bot runs both on Telegram through the **inline** @LF_Mana_Bot *rule/card* `rulename/cardname`
command and on Discord via the @ManaBot#3013 account.

---

## Update log

### March 2021

Creation of initial bot

### Between March 2021 and November 2021

Features added and optimized:
1. card image search
2. card data search
3. deck (.cod (.xml), .mwDeck) conversion (to .txt)
4. rule (keyword) search
5. rule (number) search
6. cross-platform design (Telegram and Discord)
7. dice rolling (minimal, somewhat buggy)

### November 2021 (in progress)

Conversion from dependence on Cockatrice data files to independent database

---

## Current functionality

Discord:
1. *!card* `cardname`; searches for a card's image and text and posts it
2. *!rule* `keyword/number`; searches for a rule based on a keyword (e.g. Flying) or number
   (e.g. 702.9)
3. *!roll* `XdY[dk/lh]Z+N`; rolls dice in the given format (note: buggy)
4. **attachment** *(.cod, .txt) + !checkban*; checks the attached deck against the EDH ban lists for single and
 multiplayer games
5. **attachment** *(.cod, .txt)*; converts file to .txt
6. *!help*; returns the help message

Telegram:
1. *card* `cardname`; searches for a card's image and text and posts it
2. *rule* `keyword/number`; searches for a rule based on a keyword (e.g. Flying) or number
   (e.g. 702.9)
---

## This bot is an ongoing project.
Feel free to use the inline Telegram implementation, @LF_Mana_Bot, or email me at jklilley12@gmail.com for information on how to add it to a Discord server.