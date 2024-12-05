from bs4 import BeautifulSoup as bs 
import requests 
# will not comment everything, running on hopes and dreams 

class Fetcher():
    def __init__(self) -> None:
        pass


    def getHTML(self, itemName: str) -> bs:
        item = itemName.split(' ')
        item = [(lambda x: x.capitalize() if x != 'of' else x)(i) for i in item]
        item = '_'.join(item)
        url = f"https://terraria.fandom.com/wiki/{item}"
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        print(url)
        return soup

    def alternateItens(self, itemName: str) -> str:
        if itemName == "Light's Bane" or itemName == "Blood Butcherer":
            return "Blood Butcherer or Light's Bane"
        elif itemName == "Demon Altar" or itemName == "Crimson Altar":
            return "Crimson Altar or Demon Altar"
        elif itemName == "Iron Anvil" or itemName == "Lead Anvil":
            return "Iron Anvil or Lead Anvil"
        elif itemName == "Mythril Anvil" or itemName == "Orichalcum Anvil":
            return "Mythril Anvil or Orichalcum Anvil"
        elif itemName == "Placed Bottle":
            return "Placed Bottle or Alchemy Table"
        else:
            return itemName

    def convertRarity(self, itemR: str) -> str:
        itemR = itemR[:itemR.index('*')]
        match itemR:
            case '-1':
                return 'Gray'
            case '00':
                return 'White'
            case '01':
                return 'Blue'
            case '02':
                return 'Green'
            case '03':
                return 'Orange'
            case '04':
                return 'Light Red'
            case '05':
                return 'Pink'
            case '06':
                return 'Light Purple'
            case '07':
                return 'Lime'
            case '08':
                return 'Yellow'
            case '09':
                return 'Cyan'
            case '10':
                return 'Red'
            case '11':
                return 'Purple'
            case '-12':
                return 'Rainbow'
            case '-13':
                return 'Fiery Red'
            case '-11':
                return 'Amber'
            case _:
                return itemR

    def getItemInfo(self, soup:bs) -> dict:
        itemInfo = {}
        table = soup.find('table', class_='stat')
        if table != None:
            body = table.find('tbody')
            for tr in body.find_all('tr'):
                atribute = tr.find('th').text
                if atribute == 'Research':
                    continue
                elif atribute == 'Sell':
                    continue
                if tr.find('td') != None:
                    text = tr.find('td').text
                    try :
                        text = text[:text.index('/'):]
                    except:
                        text = text
                    if atribute == 'Rarity':
                        text = self.convertRarity(text)
                    elif atribute == 'Type':
                        text = ' & '.join([tr.text for tr in tr.find_all('span', class_='nowrap')])
                    itemInfo[atribute] = text
        return itemInfo 

    def getCraftingList(self, soup: bs):
        craftingInfo = {}
        itemMade = None
        itemList = None
        itemQtds = None
        tables = soup.find_all('table', class_='recipes')
        #print(tables)
        if tables == [] and soup.find('div', class_='noarticletext') != None :
            return None
        h3s = soup.find_all("h3")
        span_tag = [h.find_all('span', {'class': 'mw-headline'}) for h in h3s]
        usedIn = []
        for s in span_tag:
            if s!= []:
                ids = s[0].get("id")    
                usedIn.append(ids) 

        i = 0
        for t in tables:
            body = t.find('tbody')         
            tr = body.find_all('tr')[1::]
            craftingStations = self.alternateItens((tr[0].find('td',class_='station').find('a', href=True).get('title')))
            #print(craftingStations)
            for tr in tr:
                #print(tr)
                result  = tr.find('td', class_='result')
                if result != None:
                    #print(result)
                    try:
                        gameVersion = result.find('div', class_='version-note').find('a', href=True).get('title')
                    except AttributeError:
                        gameVersion = 'PC Version'
                else:
                    continue
                #print(gameVersion)
                if gameVersion == 'PC version' or gameVersion == 'PC Version':
                    #print(result)
                    itemMade = result.get('data-sort-value')
                    #print(result.get('data-sort-value'))
                    #itemMade = result.find('a',href=True).get('title')
                    li = (tr.find('td', class_='ingredients').find_all('li'))
                    itemList = [self.alternateItens(li.find('a',href=True).get('title')) for li in li]
                    am = [li.find('span', class_='am') for li in li]
                    itemQtds = [am.text if am !=  None else '1' for am in am ]
                else:   
                    continue
            craftingInfo[usedIn[i]] = [itemMade,itemList,itemQtds,craftingStations]
            i += 1
            if i == len(usedIn):
                #print('end of fetcher')
                return craftingInfo
        return craftingInfo

        
    def getDropInfo(self, soup: bs) -> dict:
        dropFrom = {}
        table = (soup.find('table', class_ = "drop-noncustom"))
        if table != None:
            table = table.find('tbody')
        if table != None: 
            for t in (table.find_all('tr'))[1::]: #can't fix that error
                #print(f'\n{t}\n')
                #dropRate = t.find_all('td')[2].text
                mob = t.find('a', href = True).get('title')
                dropRate = t.find_all('td')[2].text
                try:
                    dropRate = dropRate[:dropRate.index('*')] + "%"
                except:
                    dropRate = dropRate
                dropQtd = t.find_all('td')[1].text
                dropFrom[mob] = [dropRate, dropQtd]
        #print(f'{table[0].find_all("tr", class_ ="")}\n')
        return dropFrom