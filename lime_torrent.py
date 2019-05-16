from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime


all_types = ['https://www.limetorrents.info/browse-torrents/Movies/', # Movies
 'https://www.limetorrents.info/browse-torrents/TV-shows/',           # Tv-shows
 'https://www.limetorrents.info/browse-torrents/Music/',              # Music
 'https://www.limetorrents.info/browse-torrents/Games/',              # Games
 'https://www.limetorrents.info/browse-torrents/Applications/',       # Applications
 'https://www.limetorrents.info/browse-torrents/Anime/',              # Anime
 'https://www.limetorrents.info/browse-torrents/Other/']              # Other

def make_request(url):
    page = requests.get(url)
    soup = BS(page.text,'html.parser')
    return soup


def create_date(str):
    today = datetime.date.today()
    if 'minutes' or 'hours' in str:
        return today
    elif 'Yesterday' in str:
        yesterday_date = int(today[9:]) - 1
        return today[:9] + yesterday_date
    elif 'days' in str:
        date = int(today[9:]) - int(str.split(' days ago'))
        return toady[:9] + date
    elif 'Month' in str:
        month  =  int(toady[5:7]) - 1
        return toady[0:5] + month + today[7:]

def get_links():
    filePath = 'cache/limetorrents/all_links.json'
    if os.path.exists(filePath):
        file = open(filePath)
        read_data = file.read()
        all_urls_list = json.loads(read_data)
        return all_urls_list

    all_pages_urls = []
    for type in all_types:
        soup = make_request(type)
        page_div = soup.find('div', class_='search_stat')
        all_links = page_div.find_all('a')
        total_pages_count  = int(all_links[-2].get_text())
        page_url = "https://www.limetorrents.info"+ all_links[0].get('href')[:-2]
        for i in range(1,total_pages_count+1):
            all_pages_urls.append(page_url + str(i) + '/')
    with open(filePath,'w') as file:
        text = json.dumps(all_pages_urls, sort_keys=True, indent=4)
        file.write(text)
        file.close()
    return all_pages_urls

def single_page_details(html,count):
    soup = BS(html,'html.parser')
    table = soup.find('table', class_ = 'table2')
    trs = table.find_all('tr')
    trs.pop(0)
    details_list = []
    for tr in trs:
        details_dict = {}
        details_dict['name'] = tr.find('td', class_='tdleft').div.get_text().strip()
        details_dict['hash'] = tr.find('td', class_='tdleft').a['href'].split('/torrent/')[1].split('.torrent')[0]
        date_size_tds = tr.find_all('td', class_='tdnormal')
        date_size  = [ td.get_text() for td in date_size_tds]
        seeds = tr.find('td', class_='tdseed').get_text()
        seeds = seeds.replace(',', '')
        if seeds !='0' or seeds != '-':
            details_dict['seeds'] = seeds
        details_dict['added_date'] = create_date(date_size[0]).strftime('%Y/%m/%d')
        details_dict['size'] = date_size[1]
        details_list.append(details_dict)
    path = 'cache/database/lime/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open( path+'limetorrent_' + str(count) + '_.json','w') as file:
        text = json.dumps(details_list,sort_keys=True,indent=4)
        file.write(text)
        file.close()
    return details_list
