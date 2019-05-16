from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime

def make_request(url):
    page = requests.get(url)
    soup = BS(page.text,'html.parser')
    return soup


def get_links():
	filePath = 'cache/nyaapantsu/all_links.json'
	if os.path.exists(filePath):
	    file = open(filePath)
	    read_data = file.read()
	    all_urls_list = json.loads(read_data)
	    return all_urls_list

	all_pages_urls = []
	soup = make_request("https://nyaa.pantsu.cat/")
	lastpage = soup.find("div",class_="pagination")
	nextpage = lastpage.find("a",class_="page-next")
	pages_count = int(nextpage["href"].split("/search/")[1][:-1])

	for i in range(1,pages_count+1):
		page_url = "https://nyaa.pantsu.cat/search/"+str(i)+"?"
		all_pages_urls.append(page_url)

	with open(filePath,'w') as file:
		text = json.dumps(all_pages_urls, sort_keys=True, indent=4)
		file.write(text)
		file.close()
	return all_pages_urls

def single_page_details(html,count):
    details_list = []
    soup = BS(html,"html.parser")
    tbody = soup.find("tbody",id="torrentListResults")
    trs = tbody.findAll("tr")
    for tr in trs:
        details_dict = {}
        details_dict['name'] = tr.findAll("td")[1].a.get_text().strip()
        details_dict['hash'] = (tr.findAll("td")[2].a["href"].split('magnet:?xt=urn:btih:')[1].split('&dn=')[0]).upper()
        details_dict['size'] = "".join(tr.findAll("td")[3].get_text().strip().split('i'))
        seeds = tr.findAll("td")[4].get_text().strip()
        seeds = seeds.replace(',', '')
        if seeds !='0' or seeds != '-':
            details_dict['seeds'] = seeds
        date_details = tr.findAll("td")[7]['title'].split('/')
        if len(date_details[0]) ==1:
            month = "0"+date_details[0]
        else:
            month = date_details[0]

        details_dict['added_date'] = date_details[2].split(',')[0] +'/'+ month +'/'+ date_details[1]
        details_list.append(details_dict)
    path = 'cache/database/nyaapantsu/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open( path +'nyaapantsutorrent_' + str(count) + '_.json','w') as file:
        text = json.dumps(details_list, sort_keys=True,indent=4)
        file.write(text)
        file.close()
    return details_list
