from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime

def get_links():
	all_pages_urls = []
	for i in range(1,101):
		all_pages_urls.append("https://nyaa.si/?p="+str(i))
	return all_pages_urls

def single_page_details(html,count):
	soup = BS(html,"html.parser")
	t_body = soup.find("tbody")
	trs =  t_body.findAll("tr")
	details_list = []
	for tr in trs:
		details_dict = {}
		details_dict['name'] = tr.findAll("td")[1].a.get_text().strip()
		details_dict['hash'] = (tr.findAll("td")[2].findAll('a')[1]['href'].split('magnet:?xt=urn:btih:')[1].split('&dn=')[0]).upper()
		details_dict['size'] = tr.findAll("td")[3].get_text().strip().split('i')[0] + 'B'
		date = tr.findAll("td")[4].get_text().strip()
		details_dict['added_date'] = date.replace("-","/")[:10]
		seeds = tr.findAll("td")[5].get_text().strip()
		seeds = seeds.replace(',', '')
		if seeds !='0' or seeds != '-':
			details_dict["seeds"] = seeds
		details_list.append(details_dict)
	path = 'cache/database/nyaasi/'
	if not os.path.exists(path):
		os.mkdir(path)
	with open( path +'nyaasitorrent_' + str(count) +'_.json', 'w') as file:
		text = json.dumps(details_list,sort_keys=True,indent=4)
		file.write(text)
		file.close()
	return details_list
