from bs4 import BeautifulSoup
import requests, os, time, pprint, json
from datetime import date

def get_links():
	filePath = 'cache/galaxy/all_links.json'
	if os.path.exists(filePath):
		with open(filePath) as file:
			read = file.read()
			all_urls_list = json.loads(read)
			return all_urls_list
	all_pages_urls = []
	html = requests.get("https://torrentgalaxy.org/torrents.php?")
	soup = BeautifulSoup(html.text,"html.parser")
	navs = soup.findAll("nav")[2]
	lastpage = navs.findAll("li")[-2].a.text
	for i in range(int(lastpage)+1):
		all_pages_urls.append("https://torrentgalaxy.org/torrents.php?parent_cat=&sort=id&order=desc&page="+str(i))
	with open(filePath,'w') as file:
		text = json.dumps(all_pages_urls,sort_keys= True,indent = 4)
		file.write(text)
		file.close()
	return all_pages_urls


def Create_date(taketime):
	if "H" in taketime or "M" in taketime:
		today = date.today()
		return today.strftime("%Y/%m/%d")
	else:
		taketime = taketime.split("/")
		return "20"+taketime[2]+"/"+taketime[1]+"/"+taketime[0]

def single_page_details(html,count):
	soup = BeautifulSoup(html,"html.parser")
	divs = soup.findAll("div",class_="tgxtablerow")
	details_list = []
	for d in divs:
		details_dict = {}
		magnetdiv = d.findAll("div")[5]
		atag = magnetdiv.findAll("a")[1]
		details_dict['hash'] = atag["href"].split('magnet:?xt=urn:btih:')[1].split('&dn=')[0].upper()
		details_dict['name'] = d.findAll("div")[3].text.strip()#name
		details_dict['size'] = d.findAll("div")[8].text.strip()#Size
		seed_and_leech = d.findAll("div")[11].text.strip()#seed
		seed = seed_and_leech.strip("[").strip("]").split("/")[0]
		if seed != "0" or seeds !='-':
			details_dict["seeds"] = seed
		created = d.findAll("div")[12].text.strip().split()[0]#added
		details_dict['added_date'] = Create_date(created)
		details_list.append(details_dict)
	path = 'cache/database/galaxy/'
	if not os.path.exists(path):
		os.mkdir(path)
	with open(path + 'galaxytorrent_' + str(count) + '_.json','w') as file:
		text = json.dumps(details_list,sort_keys=True,indent=4)
		file.write(text)
		file.close()
	return details_list
