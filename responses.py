import random
import asjdasd
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
            mode = info[0]
            thing = info[1]
            match mode: 
                case mode if "crafting" in mode:
                    data = asjdasd.getCraftingList(asjdasd.getHTML(thing))
                    print(data)
                    return self.getStringCrafting(data, thing)
                case mode if "drop" in mode:
                    data = fetcher.getDropInfo(asjdasd.getHTML(thing))
                    print(data)
                    return self.getStringDrop(data, thing)
                case mode if "boss" in mode:
                    return None
                case mode if "item" in mode:
                    return None
                case mode if "info" in mode:
                    return None
                case mode if "help" in mode:
                    text ='''
                          Welcome to terra helper!!
                          Modes:
                          !item -> Returns the item atributes
                          !crafting -> Returns the item crafint list, how to make and items made by
                          !drop -> Returns where the item can be obtained 
                          !info -> Return all of the above 

                          Extra:
                          d[6,12,100] -> return a random int like a dice
                          coin or coin flip -> Return 0 or 1
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

    def getStringCrafting(self, dictCraft: dict, itemName: str):
        text = ''
        for k in dictCraft:
            text += f'\n ##       {k.replace('_', ' ')}: {dictCraft[k][0]}. \n ### Using: \n'
            for i in range(len(dictCraft[k][1])):
                text += f'>         - {dictCraft[k][1][i]} x {dictCraft[k][2][i]} ;\n'
            text += f'### Crafting station: {dictCraft[k][3]}'
        return text


    def getStringDrop(self, dropList: dict, itemName: str):
        text = ''
        text += f'{itemName.capitalize()}, Found on:'
        for k in dropList:
            text += f'\n>    - {k}; {dropList[k][0]}; Qtd: {dropList[k][1]};'
        return text
