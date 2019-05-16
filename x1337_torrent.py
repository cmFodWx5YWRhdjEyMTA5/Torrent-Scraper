from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime


all_types = ['https://1337x.to/cat/Movies/', # Movies
 'https://1337x.to/cat/TV/',              # Tv-shows
 'https://1337x.to/cat/Music/',           # Music
 'https://1337x.to/cat/Games/',           # Games
 'https://1337x.to/cat/Apps/',            # Applications
 'https://1337x.to/cat/Anime/',           # Anime
 'https://1337x.to/cat/Documentaries/',   # Documentaries
 'https://1337x.to/cat/Other/',           # Other
 'https://1337x.to/cat/XXX/']             # Adult

def make_request(url):
    page = requests.get(url)
    soup = BS(page.text,'html.parser')
    return soup

def create_date(date_list):
    month = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','June':'6',
    'July':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}

    if len(date_list) == 1:
        today = datetime.date.today().strftime('%Y/%m/%d')
        return today
    elif len(date_list) == 3:
        strmonth = date_list[1].split('.')[0]
        if 'st' in date_list[-1]:
            day = date_list[-1].split('st')
            if len(month[strmonth]) == 1:
                date = '2019/' + '0'+ month[strmonth] +'/'+ day[0]
                return date
            date = '2019/' + month[strmonth] +'/'+ day[0]
            return date
        elif 'th' in date_list[-1]:
            day = date_list[-1].split('th')
            if len(month[strmonth]) == 1:
                date = '2019/' + '0'+ month[strmonth] +'/'+ day[0]
                return date
            date = '2019/' + month[strmonth] +'/'+ day[0]
            return date
        elif 'nd' in date_list[-1]:
            day = date_list[-1].split('nd')
            if len(month[strmonth]) == 1:
                date = '2019/' + '0'+ month[strmonth] +'/'+ day[0]
                return date
            date = '2019/' + month[strmonth] +'/'+ day[0]
            return date
        elif 'rd' in date_list[-1]:
            day = date_list[-1].split('rd')
            if len(month[strmonth]) == 1:
                date = '2019/' + '0'+ month[strmonth] +'/'+ day[0]
                return date
            date = '2019/' + month[strmonth] +'/'+ day[0]
            return date



def get_links():
    all_pages_urls = []
    for type in all_types:
        for count in range(1,151):
            all_pages_urls.append(type + str(count) + '/')
    return all_pages_urls

def single_page_details(html,count):
    soup = BS(html,'html.parser')
    table = soup.find('table', class_ = 'table-responsive').tbody
    trs = table.find_all('tr')
    details_list = []
    for tr in trs:
        details_dict = {}
        link = tr.find('td', class_='coll-1').findAll("a", recursive=False)[1]['href']
        soup = make_request("https://1337x.to" + link)
        hash = soup.find('div', class_='infohash-box').span.get_text().strip()
        details_dict['name'] = tr.find('td', class_='coll-1').get_text().strip()
        details_dict['hash'] = hash
        seeds = tr.find('td', class_='coll-2').get_text()
        seeds = seeds.replace(',', '')
        if seeds !='0' or seeds != '-':
            details_dict['seeds'] = seeds
        date_list = tr.find('td', class_='coll-date').get_text().split()
        date = create_date(date_list)
        details_dict['added_date'] = date
        details_dict['size'] = tr.find('td', class_='coll-4').get_text().split('B')[0] + 'B'
        details_list.append(details_dict)
    path = 'cache/database/x1337/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open( path +'x1337torrent_' + str(count) +'_.json', 'w') as file:
        text = json.dumps(details_list,sort_keys=True,indent=4)
        file.write(text)
        file.close()
    return details_list
