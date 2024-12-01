from bs4 import BeautifulSoup as bs 
import requests 
# will not comment everything, running on hopes and dreams 

def getHTML(itemName: str) -> bs:
    item = itemName.split(' ')
    item = [i.capitalize() for i in item]
    item = '_'.join(item)
    url = f"https://terraria.fandom.com/wiki/{item}"
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    print(url)
    return soup

def getCraftingListAlt(soup: bs) -> dict:
    craftingInfo = {}
    # get the crafting modes that the item have 
    h3s = soup.find_all("h3")
    span_tag = [h.find_all('span', {'class': 'mw-headline'}) for h in h3s]
    usedIn = []
    for s in span_tag:
        if s!= []:
            ids = s[0].get("id")
            usedIn.append(ids) 
    print(usedIn)

    tables = soup.find_all('table', class_ = 'recipes')
    i = 0
    for t in tables:    
        tr = t.find('tbody')
        #all right
        for tr in tr.find_all('tr'):
            # Gets crafting station
            if tr.find('td',{"class":['station']}) != None: 
                print('here0')
                stations = [x.get('title') for x in tr.find('td',{"class":['station','data-sort-value']}).find_all('a', href=True)]
                stations = list(set(stations))
            # Handles diferent tables for diferent game versions    
            if tr.find('div', class_='version-note')!= None and (tr.find('div', class_='version-note').find('a', href = True).get('title')) != 'Old-gen console version':
                print('here1')
                itemCrafted = tr.find('td', class_='result').get('data-sort-value')
                li = tr.find('td', class_='ingredients').find_all('li')
                am = [li.find('span', class_='am') for li in li]
                ingredients = [(l.find('a',href = True).get('title')) for l in li]
                itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]
                
            elif tr.find('span', class_='eico') != None and "PC, Console" in str(tr.find('span', class_='eico').get('title')):
                print('here2')
                itemCrafted = tr.find('a', href=True).get('title')  
                li = tr.find('td', class_='ingredients').find_all('li')
                am = [li.find('span', class_='am') for li in li]
                ingredients = [(l.find('a',href = True).get('title')) for l in li]
                itemQtds = [(lambda x: 1 if x == None else x.text)(x) for x in am]

            elif tr.find('span', class_='eico') == None and tr.find('div', class_='version-note') == None:
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
        #print(craftingInfo)
        i += 1
        if i == len(usedIn):
            return craftingInfo
    return craftingInfo 
    
def getDropInfo(soup: bs) -> dict:
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
print((getCraftingListAlt(getHTML("bookcases"))))
#print(getDropInfo(getHTML('Bee keeper')))
