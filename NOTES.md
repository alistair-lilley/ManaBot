    ## quick notes for reference

### json card data
1. DO NOT LOSE THIS LINK: `https://mtgjson.com/api/v5/AllPrintings.json`

2. DO NOT LOSE THIS LINK: `https://gatherer.wizards.com/Handlers/Image.ashx?name=!name!&type=card`

Link 1. is the direct link to downloading all card JSONs

Link 2. is the direct link to downloading each card image. Replace !name! with the name of the card.

The json card data is structured as such:

*Top level:* `{ meta, data }`

*Under data:* `{ dict of card sets }`

*Under each card set:* `{ 'baseSetSize', 'block', 'booster', 'cards', 'code', 'isFoilOnly', 'isOnlineOnly', 'keyruneCode', 'mcmId', 'mcmName', 'mtgoCode', 'name', 'releaseDate', 'sealedProduct', 'tcgplayerGroupId', 'tokens', 'totalSetSize', 'translations', 'type' }`

*Under cards:* `[ list/array of card dicts ]`

*Individual cards:* `{ 'artist', 'availability', 'borderColor', 'colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'finishes', 'foreignData', 'frameVersion', 'hasFoil', 'hasNonFoil', 'identifiers', 'isReprint', 'keywords', 'layout', 'legalities', 'manaCost', 'name', 'number', 'originalText', 'originalType', 'power', 'printings', 'purchaseUrls', 'rarity', 'rulings', 'setCode', 'subtypes', 'supertypes', 'text', 'toughness', 'type', 'types', 'uuid', 'variations' }`

The things we'll want to focus on are:
`AllPrintings['data']['CARDSETCODE']['cards'][indexed cards][ ... ]`
    [ ... ] includes: 
- colorIdentity
- colors 
- convertedManaCost
- kewyords?
- manaCost
- name
- number
- power
- text
- toughness
- type
- types
- uuid

### update: there might be others i missed
