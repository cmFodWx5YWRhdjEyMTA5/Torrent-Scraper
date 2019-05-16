from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime

all_types = [
    'https://glodls.to/search.php?cat=1',  # Movies
    'https://glodls.to/search.php?cat=41', # Tv
    'https://glodls.to/search.php?cat=18', # Softwears / Apps
    'https://glodls.to/search.php?cat=22', # Music
    'https://glodls.to/search.php?cat=50', # Adults
    'https://glodls.to/search.php?cat=10', # Games
    'https://glodls.to/search.php?cat=51', # books
    'https://glodls.to/search.php?cat=28',  # Anime
    'https://glodls.to/search.php?cat=52', # Mobile Apps
    'https://glodls.to/search.php?cat=71',  # Video
    'https://glodls.to/search.php?cat=70',  # Pictures
    'https://glodls.to/search.php?cat=72'  # TV / MOVIE PACKS
    ]

def make_request(url):
    page = requests.get(url)
    soup = BS(page.text,'html.parser')
    return soup

def get_links():
    filePath = 'cache/glodls/all_links.json'
    if os.path.exists(filePath):
        file = open(filePath)
        read_data = file.read()
        all_urls_list = json.loads(read_data)
        return all_urls_list

    all_pages_urls = []
    for type in all_types:
        count = type.split('https://glodls.to/search.php?cat=')
        soup = make_request(type)
        page_div = soup.find('div', class_='pagination')
        all_links = page_div.find_all('a')
        if len(all_links) != 0:
            total_pages_count  = int(all_links[-2].get('href').split('/search_results.php?cat=' + str(count[-1]) + '&sort=id&order=desc&page=')[1])
        else:
            all_pages_urls.append(type)
        url = 'https://glodls.to/search_results.php?cat=1&sort=id&order=desc&page='
        for i in range(1,total_pages_count+1):
            all_pages_urls.append(url + str(i))

    with open(filePath,'w') as file:
        text = json.dumps(all_pages_urls, sort_keys=True, indent=4)
        file.write(text)
        file.close()
    return all_pages_urls

def single_page_details(html,index):
    soup = BS(html,'html.parser')
    table = soup.find('table', class_ = 'ttable_headinner')
    trs = table.find_all('tr', recursive=False)
    details_list = []
    trs.pop(0)
    count = 1
    for tr in trs:
        if count % 2 ==0:
            details_dict = {}
            all_tds = tr.find_all('td', recursive=False)
            details_dict['name'] = all_tds[1].get_text().strip()
            details_dict['hash'] = all_tds[3].a['href'].split(":btih:")[1].split("&dn=")[0]
            seeds = all_tds[5].get_text()
            seeds = seeds.replace(',', '')
            if seeds !='0' or seeds != '-':
                details_dict['seeds'] = seeds
            details_dict['size'] = all_tds[4].get_text()
            details_list.append(details_dict)
        count+=1
    path = 'cache/database/glodls/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open( path + 'glodlstorrent_' + str(index) + '_.json','w') as file:
        text = json.dumps(details_list,sort_keys=True,indent=4)
        file.write(text)
        file.close()
    return details_list
