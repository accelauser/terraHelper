from bs4 import BeautifulSoup as bs
import requests 
import gc # memory managment 
# https://stackoverflow.com/questions/1316767/how-can-i-explicitly-free-memory-in-python

def getHTML(itemName: str) -> bs:
    item = itemName.split(' ')
    item = [(lambda x: x.capitalize() if x != 'of' else x)(i) for i in item]
    item = '_'.join(item)
    url = f"https://terraria.fandom.com/wiki/{item}"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    print(url)
    return soup

def getCraftingList(soup: bs) -> dict:
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
        craftingStations = alternateItens((tr[0].find('td',class_='station').find('a', href=True).get('title')))
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
                itemList = [alternateItens(li.find('a',href=True).get('title')) for li in li]
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


def alternateItens(itemName: str) -> str:
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
#   print(getCraftingList(getHTML("Copper shortsword")))



