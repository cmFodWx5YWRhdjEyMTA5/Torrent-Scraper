import asyncio
import requests, time, aiohttp, json, pprint,mydb
import lime_torrent, glodls_torrent, thepiratebay_torrent,x1337_torrent
import nyaasi_torrent, anidex_torrent, nyaapantsu_torrent, evztv_torrent
import galaxy_torrent
from random import randint


torrent_services = [
    'thepiratebay_torrent',
    'nyaasi_torrent',
    'nyaapantsu_torrent',
    'evztv_torrent',
    'glodls_torrent',
    'galaxy_torrent',
    'lime_torrent',
    'x1337_torrent',
    'anidex_torrent'
    ]

http_proxy  = ['http://95.215.97.203','http://95.161.9.41','http://95.170.220.172']
proxyDict = {
              "http"  : 'http://95.215.97.203',

            }

async def call_url(url, types, count):
    print('Starting {}'.format(url))
    nap = randint(0,3)
    await asyncio.sleep(nap)
    resp = requests.get(url, proxies=proxyDict)
    data = resp.text
    details = eval(types).single_page_details(data, count)
    pprint.pprint(details)
    return details


def fetch(type):
    try:
        urls = eval(type).get_links()
        start = time.time()
        count = 0
        while True:
            futures = []
            for url in urls[:500]:
                count+=1
                futures.append(call_url(url, type, count))

            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(futures))
            del urls[0:500]
            if len(urls) == 0:
                insert = mydb.readFile(type.split('_torrent')[0])
                print("*" * 100)
                print("Database inserted successfully")
                print("*" * 100)
                break
            # loop.close()
    except ValueError:
        pass

for torrent in torrent_services:
    fetch(torrent)
