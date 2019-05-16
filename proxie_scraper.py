from bs4 import BeautifulSoup as BS
import requests, os, pprint, json

def get_links():
    all_links = []
    for i in range(265):
        url = 'http://www.hidemyassproxylist.org/?field=id&order=asc&page=' + str(i)
        all_links.append(url)
    return all_links

url_list = get_links()

def get_proxies(url_list):

    proxy_list = []

    for url in url_list:
        print(url)
        try:
            page = requests.get(url)
            soup = BS(page.text,'html.parser')
            main_div = soup.find('div',class_='striped-table')
            table = main_div.find('table', class_='striped').tbody
            trs = table.findAll('tr')
            for tr in trs:
                proxy = tr.findAll('td')[1].get_text().strip()
                proxyDict = {
                    'http': proxy
                }
                proxy_list.append(proxyDict)
        except AttributeError:
            pass
    path = 'cache/proxy/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open( path +'proxy.json','w') as file:
        text = json.dumps(proxy_list,sort_keys=True,indent=4)
        file.write(text)
        file.close()

    return proxy_list

a = get_proxies(url_list)
pprint.pprint(a)
