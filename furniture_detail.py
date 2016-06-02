import urllib.request as fetch
import re
from time import sleep
from random import random
from pymongo import MongoClient as mc


ikea = 'http://www.ikea.com'
client = mc()
db = client.IKEA
furniture = db.core_furniture
todo=furniture.find({'done':2})
i=todo.count()
for each in todo:
    _id = str(each['id'])
    print(_id)
    sleep(2 * random())
    url = 'http://www.ikea.com/cn/zh/catalog/products/' + _id
    try:
        response = fetch.urlopen(url)
        response = response.read().decode('utf8')
        pattern_name = re.compile(
            '<div id="name" class="productName">(.*?)</div>.*?<div id="type" class="productType">(.*?)<strong>', re.S)
        pattern_price = re.compile('<span id="price1" class="packagePrice">(.*?)</span>', re.S)
        pattern_img = re.compile('<img id="productImg" src=\'(.*?)\'.*?title=.*?>', re.S)
        result_name_type = re.findall(pattern_name, response)
        result_price = re.findall(pattern_price, response)
        result_img = re.findall(pattern_img, response)
        print(result_name_type)
        print(result_img)
        print(result_price)
        print(len(result_name_type))
        if(result_name_type):
            if len(result_name_type[0]) > 1:
                name = result_name_type[0][0].strip()
                ftype = result_name_type[0][1].strip()
                print(name, ftype)
                furniture.update_one({'id':_id},{'$set':{'name': name, 'type': ftype, 'done':1}})
        if result_img:
            img = ikea + result_img[0]
            filename = _id + ".jpg"
            fetch.urlretrieve(img, filename)
    except:
        furniture.update_one({'id':_id},{'$set':{'done':2}})
