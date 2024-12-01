import random

from fetcher import getCraftingListAlt, getDropInfo, getHTML 

#https://www.youtube.com/watch?v=DnFP0MRJPIg
def handle_responses(message):
    lMessage = message.lower()
    if message[0] == '!':
        info = lMessage[1::].split(maxsplit=1)
        mode = info[0]
        thing = info[1]
        match mode: 
            case mode if "item" in mode:
                data = getCraftingListAlt(getHTML(thing))
                #print(data)
                return getStringCrafting(data)
            case mode if "drop" in mode:
                data = getDropInfo(getHTML(thing))
                #print(data)
                return getStringDrop(data)
            case mode if "boss" in mode:
                return None
            case _:
                return 'Lol dum b fuckers'
    else:
    
        if "d6" in lMessage:
            return str(random.randint(1,6))
        elif "d12" in lMessage:
            return str(random.randint(1,12))
        elif "d100" in lMessage:
            return str(random.randint(1,100))
        elif "coin" in lMessage or "coin flip" in lMessage:
            return str(random.randint(0,1))
        else:
            return "idk"

def getStringCrafting(dictCraft: dict):
    text = ''
    for k in dictCraft:
        text += f'\n{k}: {dictCraft[k][0]}. \nUsing: '
        for i in range(len(dictCraft[k][1])):
            text += f'\n    {dictCraft[k][1][i]} x {dictCraft[k][2][i]}; '
        text += f'\nCrafting station: '
        endInt = len(dictCraft[k][3])
        for i in range(endInt):
            if i != endInt-1:
                text += f'{dictCraft[k][3][i]} or '
            else:
                text += f'{dictCraft[k][3][i]}.\n'
    return text


def getStringDrop(dropList: dict):
    text = ''
    for k in dropList:
        text += f'Mob: {k}. Chance: {dropList[k][0]}. Quantity: x{dropList[k][1]}\n'
    return text

print(getStringDrop({'Queen Bee': ['33%', '1'], 'Treasure Bag (Queen Bee)': ['33%', '1']}))
print(getStringCrafting({'Recipes': ['Copper Shortsword', ['Copper Bar'], ['5'], ['Iron Anvil', 'Lead Anvil']], 'Used_in': ['Zenith', ['Terra Blade', 'Meowmere', 'Star Wrath', 'Influx Waver', "The Horseman's Blade", 'Seedler', 'Starfury', 'Bee Keeper', 'Enchanted Sword', 'Copper Shortsword'], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ['Orichalcum Anvil', 'Mythril Anvil']]}))