from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime

def make_request(url):
    page = requests.get(url)
    soup = BS(page.text,'html.parser')
    return soup

def get_links():
	filePath = 'cache/anidex/all_links.json'
	if os.path.exists(filePath):
	    file = open(filePath)
	    read_data = file.read()
	    all_urls_list = json.loads(read_data)
	    return all_urls_list

	all_pages_urls = []
	soup = make_request("https://anidex.info/")
	all_links = soup.find("nav",class_="text-center")
	pages_count = int(all_links.findAll("a")[-1]['href'].split('/?offset=')[1])
	for i in range(pages_count+1):
		page_url = "https://anidex.info/?offset=" + str(i)
		all_pages_urls.append(page_url)

	with open(filePath,'w') as file:
		text = json.dumps(all_pages_urls, sort_keys=True, indent=4)
		file.write(text)
		file.close()
	return all_pages_urls

def single_page_details(html,count):
    soup = BS(html,"html.parser")
    tbody = soup.find("tbody")
    trs = tbody.findAll("tr")
    details_list = []
    for tr in trs:
        details_dict = {}
        details_dict['name'] = tr.find("a",class_="torrent").findAll('span')[0].get_text().strip()
        details_dict['hash'] = tr.findAll("td")[5].a['href'].split('magnet:?xt=urn:btih:')[1].split('&tr=')[0].strip()
        details_dict['size'] = tr.findAll("td")[6].get_text().strip()
        details_dict['added_date'] = tr.findAll("td")[7]["title"][:10].strip().replace('-','/')
        seeds = tr.findAll("td")[8].get_text().strip()
        seeds = seeds.replace(',', '')
        if seeds !='0' or seeds != '-':
            details_dict['seeds'] = seeds
            details_list.append(details_dict)
    path = 'cache/database/anidex/'
    if not os.path.exists(path):
        os.mkdir(path)
    file = open( path+'anidextorrent_' + str(count) + '_.json','w')
    text = json.dumps(details_list, sort_keys=True, indent = 4)
    file.write(text)
    file.close()

    return details_list
