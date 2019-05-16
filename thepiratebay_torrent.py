from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime


all_types = ['https://thepiratebay.org/browse/100/',  # Audio
 'https://thepiratebay.org/browse/200/',              # Video
 'https://thepiratebay.org/browse/300/',              # Applications
 'https://thepiratebay.org/browse/400/',              # Games
 'https://thepiratebay.org/browse/500/',              # Adult
 'https://thepiratebay.org/browse/600/']              # Other

def create_date(string):
    today = datetime.date.today().strftime('%Y/%m/%d')
    if 'Today' in string:
        return today
    elif 'Y-day' in string:
        yesterday_date = int(today[9:]) - 1
        return today[:9] + str(yesterday_date)
    else:
        return today[:4] +'/'+ string.replace('-','/')

def get_links():
    all_pages_urls = []
    for type in all_types:
        for i in range(45):
            url = type + str(i) + '/3'
            all_pages_urls.append(url)
    return all_pages_urls

def single_page_details(html,count):
    soup = BS(html,'html.parser')
    main_container = soup.find('div', attrs = {'id':'main-content'})
    table = main_container.find('table', attrs = {'id':'searchResult'})
    trs = table.find_all('tr', recursive=False)
    if len(trs) <= 1:
        return
    trs.pop(-1)
    details_list = []
    for tr in trs:
        details_dict = {}
        tds = tr.find_all('td')
        details_dict['name'] =  tds[1].div.a.get_text().strip()
        details_dict['hash'] =  (tds[1].findAll('a')[1]['href'].split('magnet:?xt=urn:btih:')[1].split('&dn=')[0]).upper()
        seeds = tds[2].get_text()
        seeds = seeds.replace(',', '')
        if seeds != '0' or seeds != '-':
            details_dict['seeds'] = seeds
        date = tds[1].font.get_text().strip().split('Uploaded ')[1].split(', Size')[0][:5]
        print('*' * 100,date)
        details_dict['added_date'] = create_date(date)
        details_dict['size'] = " ".join(tds[1].font.get_text().strip().split('Size ')[1].split(', ULed by')[0].split('i')[0].split('\xa0')) + 'B'
        details_list.append(details_dict)
    path =  'cache/database/thepiratebay/'
    if not os.path.exists(path):
        os.mkdir(path)

    file = open( path +'thepiratebaytorrent_' + str(count) + '_.json','w')
    text = json.dumps(details_list, sort_keys=True, indent = 4)
    file.write(text)
    file.close()
    return details_list
