from bs4 import BeautifulSoup as bs 
import requests 
# will not comment everything, running on hopes and dreams 

class Fetcher():
    def __init__(self) -> None:
        pass

    def getHTML(self, itemName: str) -> bs:
        item = itemName.split(' ')
        item = [i.capitalize() for i in item]
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

    def getCraftingList(self, soup: bs) -> dict:
        craftingInfo = {}
        tables = soup.find_all('table', class_='recipes')
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
                        print('here0')
                        gameVersion = 'PC Version'
                else:
                    continue
                #print(gameVersion)
                if gameVersion == 'PC version' or gameVersion == 'PC Version':
                    print('heregamev')
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
                print('end of fetcher')
                return craftingInfo
        return craftingInfo
    # Dont really work well, might delete later 
    def getCraftingListAlt(self, soup: bs) -> dict:
        craftingInfo = {}
        # get the crafting modes that the item have 
        h3s = soup.find_all("h3")
        span_tag = [h.find_all('span', {'class': 'mw-headline'}) for h in h3s]
        usedIn = []
        for s in span_tag:
            if s!= []:
                ids = s[0].get("id")    
                usedIn.append(ids) 

        tables = soup.find_all('table', class_ = 'recipes')
        i = 0
        for t in tables:    
            body = t.find('tbody')
            #print(body)
            #all right

            for tr in body.find_all('tr'):
                #print(tr)
                #print(tr.find('span', class_='eico'))
                #print(body.find('div', class_='version-note') != None) 
                #print(body.find('div', class_='version-note').find('a', href=True).get('title'))
                # Gets crafting station
                if body.find('td',{"class":['station']}) != None: 
                    '''
                    print('here0')
                    stations = [x.get('title') for x in body.find('td',{"class":['station','data-sort-value']}).find_all('a', href=True)]
                    stations = list(set(stations))
                    '''
                    stations = None
                # Handles diferent tables for diferent game versions    
                if body.find('div', class_='version-note')!= None and (body.find('div', class_='version-note').find('a', href = True).get('title')) != 'Old-gen console version':
                    print('here1')
                    itemCrafted = tr.find('td', class_='result').get('data-sort-value')
                    li = tr.find('td', class_='ingredients').find_all('li')
                    am = [li.find('span', class_='am') for li in li]
                    ingredients = [(l.find('a',href = True).get('title')) for l in li]
                    itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]
                    
                elif body.find('span', class_='eico') != None and "PC, Console" in str(body.find('span', class_='eico').get('title')):
                    print('here2')
                    itemCrafted = tr.find('a', href=True).get('title')  
                    li = tr.find('td', class_='ingredients').find_all('li')
                    am = [li.find('span', class_='am') for li in li]
                    ingredients = [(l.find('a',href = True).get('title')) for l in li]
                    itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]

                elif body.find('span', class_='eico') == None and body.find('div', class_='version-note') == None:
                    print('here3')
                    # print(t.find('tbody'))
                    body = t.find('tbody')
                    #print(body.find_all('tr'))
                    itemCrafted = []
                    for tr in body.find_all('tr'):
                        if tr.find('td', class_ = 'result') != None:
                            itemCrafted.append((tr.find('td', class_ = 'result').find('img')['title']))
                            # Dont work for everyone 
                    ing = body.find_all('td', class_='ingredients')
                    ingredients = [i.find('a', href = True).get('title') for i in ing]
                    am = [li.find('span', class_='am') for li in ing]
                    itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]
        


            craftingInfo[usedIn[i]] = [itemCrafted, ingredients, itemQtds, stations]
            print(craftingInfo)
            i += 1
            if i == len(usedIn):
                return craftingInfo
        return craftingInfo 
        
    def getDropInfo(self, soup: bs) -> dict:
        dropFrom = {}
        table = (soup.find('table', class_ = "drop-noncustom")).find('tbody') 
        #print(table)
        for t in table.find_all('tr')[1::]:
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



#print(getHTML('bee keeper'))
#print((getCraftingListAlt(getHTML("bookcases"))))
#print(getDropInfo(getHTML('Bee keeper')))
