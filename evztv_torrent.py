from bs4 import BeautifulSoup  as BS
import requests, os, time, pprint, json
import datetime

def get_links():
	all_pages_urls = []
	for i in range(4314):
		page_url = "https://eztv.io/page_"+str(i)
		all_pages_urls.append(page_url)
	return all_pages_urls

def single_page_details(html,count):
	details_list = []
	soup = BS(html,"html.parser")
	table = soup.findAll("table")[9]
	trs = table.findAll("tr")
	for tr in trs:
		details_dict = {}
		all_months_list = [' January', ' February',
		' March', ' April', ' May', ' June',
		' July', ' August', ' September', ' October', ' November', ' December']
		if tr.find("td",class_="header_date"):
			date = tr.find("b").get_text().strip()
			month_in_words = date.strip().split(",")
			month = month_in_words[1]
		if tr.find("td",class_="forum_thread_post"):
			name = tr.findAll("td")[1].text.strip()
			hash = tr.findAll("td")[2].find("a")["href"].split("magnet:?xt=urn:btih:")[1].split("&dn=")[0].strip()
			size = tr.findAll("td")[3].text.strip()
			seeds = tr.findAll("td")[5].text.strip()

			if month in all_months_list:
				month_in_number = all_months_list.index(month)+1
				if len(str(month_in_number)) ==1:
					month_in_number = "0"+str(month_in_number)
				else:
					month_in_number = month_in_number
				date = month_in_words[2]+"/"+str(month_in_number)+"/"+month_in_words[0]
				details_dict = {"name":name,"hash":hash.upper(),"size":size,"added_date":date.strip()}
			if seeds != "-" or seeds != '0':
				details_dict["seeds"] = seeds

			details_list.append(details_dict)
	path = 'cache/database/evztv/'
	if not os.path.exists(path):
		os.mkdir(path)
	with open( path +'evztvtorrent_' + str(count) + '_.json','w') as file:
		text = json.dumps(details_list,sort_keys=True,indent=4)
		file.write(text)
		file.close()

	return details_list
