import random
from fetcher import Fetcher
fetcher = Fetcher()

class Handler():
    def __init__(self) -> None:
        pass

    #https://www.youtube.com/watch?v=DnFP0MRJPIg
    def handle_responses(self, message):
        lMessage = message.lower()
        if message[0] == '!':
            info = lMessage[1::].split(maxsplit=1)
            if len(info) > 1:
                mode = info[0]
                thing = info[1]
            else:
                mode = info[0]
                thing = 'None'
            match mode:     
                case mode if "crafting" in mode:
                    data = fetcher.getCraftingList(fetcher.getHTML(thing))
                    if data == None:
                        return "Could not find the item"
                    print(data)
                    return self.getStringCrafting(data)

                case mode if "drop" in mode:
                    data = fetcher.getDropInfo(fetcher.getHTML(thing))
                    if data == None:
                        return "Could not find the item"
                    print(data)
                    return self.getStringDrop(data)
                
                case mode if "boss" in mode:
                    return None

                case mode if "info" in mode:
                    data = fetcher.getItemInfo(fetcher.getHTML(thing))
                    return self.getStringInfo(data)

                case mode if "item" in mode:
                    html = fetcher.getHTML(thing)

                    drop = fetcher.getDropInfo(html)
                    craft = fetcher.getCraftingList(html)
                    info = fetcher.getItemInfo(html)
                    print(drop)
                    print(craft)
                    print(info)
                    if drop == None or craft == None:
                        return "Could not find the item"
                    return (self.getStringInfo(info) + self.getStringCrafting(craft) + self.getStringDrop(drop))

                case mode if "help" in mode:
                    text ='''
                          Welcome to terra helper!!
Modes:
> !info -> Returns the item atributes
> !crafting -> Returns the item crafint list, how to make and items made by
> !drop -> Returns where the item can be obtained 
> !item -> Return all of the above 

Extra:
> d[6,12,100] -> return a random int like a dice
> coin or coin flip -> Return 0 or 1
                          '''
                    return text
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

    def getStringCrafting(self, dictCraft: dict):
        text = ''
        for k in dictCraft:
            text += f'\n## {k.replace('_', ' ')}: {dictCraft[k][0]}. \n ### Using: \n'
            for i in range(len(dictCraft[k][1])):
                text += f'>         - {dictCraft[k][1][i]} x {dictCraft[k][2][i]} ;\n'
            text += f'### Crafting station: {dictCraft[k][3]}'
        return text

    def getStringDrop(self, dropList: dict):
        text = ''
        if dropList == {}:
            text += '\n### Found on:'
            text += "\nCan't be dropped"
            return text
        
        text += '\n## Found on:'
        for k in dropList:
            text += f'\n>    - {k}; {dropList[k][0]}; Qtd: {dropList[k][1]};'
        return text

    def getStringInfo(self, itemInfo: dict) -> str:
        text = ''
        text += '## Item information: \n'
        for k in itemInfo:
            text += f'>    - {k}: {itemInfo[k]}\n'
        return text
