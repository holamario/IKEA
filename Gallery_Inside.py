from pymongo import MongoClient as mc
import re
import urllib.request as fetch
from time import sleep
import random

client=mc()
db=client.IKEA
gallery_gadget=db.GalleryGadget
gallery_url=db.GalleryUrl
tobe=gallery_url.find({'iscrawled':2})
#gallery_url.update_many({},{'$set':{'iscrawled':0}})
numbers=tobe.count()
for each in tobe:
    print(numbers)
    sleep(random.random()*2)
    gadgat=[]
    url=each['url']
    response=fetch.urlopen(url)
    response=response.read().decode('utf8')
    print(response)
    #pattern_gadget=re.compile('<a title=".*?" href="/cn/zh/catalog/products/(.*?)/">',re.S)
    pattern_gadget=re.compile('href="/cn/zh/catalog/products/(.*?)/',re.S)
    result=re.findall(pattern_gadget,response)
    print(result)
    if(result):
        for each in result:
            if each not in gadgat:
                gadgat.append(each)
                print(each)
                print(url)
                #gallery_gadget.insert_one({'gadgetid':each,'upper':url})
        gallery_gadget.insert_one({'gadgetid':gadgat,'upper':url})
        gallery_url.update_one({'url':url},{'$set':{'iscrawled':1}})
    else:
        gallery_url.update_one({'url':url},{'$set':{'iscrawled':2}})
    numbers-=1
'''pattern=re.compile('<div class="image">(.*?)</div>',re.S)
    result=re.findall(pattern,response)
    if(result):
        gadget_html=result[0]
        pattern_gadget=re.compile('<a title=".*?" href="/cn/zh/catalog/products/(.*?)/">',re.S)
        result_gadget=re.findall(pattern_gadget,gadget_html)
        if(result_gadget):
            for each in result_gadget:
                gallery_gadget.insert_one({'gadgetid':each,''})'''