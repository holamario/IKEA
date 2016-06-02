def gallery_spider(url,type):
    import urllib.request as fetch
    import re
    from pymongo import MongoClient as mc
    import urllib

    response=fetch.urlopen(url)
    response=response.read().decode('utf8')
    pattern=re.compile('<div class="roomblock.*?">(.*?)</div>',re.S)
    results=re.findall(pattern,response)
    ikea='http://www.ikea.com'
    i=0
    client=mc()
    db=client.IKEA
    gallery_url=db.GalleryUrl
    gallery_url.update_many({},{'$set':{'iscrawled':0}})
    for room in results:
        #print(room)
        pattern_url=re.compile('<a title=".*?" href="(.*?)">',re.S)
        pattern_img=re.compile('<img alt=".*?" title=".*?" src="(.*?)".*?>')
        result_url=re.findall(pattern_url,room)
        result_img=re.findall(pattern_img,room)
        if(result_url):
            room_url=ikea+result_url[0]
            gallery_url.insert_one({'type':type,'url':room_url,'iscrawled':0})
        if(result_img):
            room_img=ikea+result_img[0]
            filename=type+'_'+str(i)+".jpg"
            urllib.request.urlretrieve(room_img, filename)

            i += 1
        print(room_url,room_img)

url=['http://www.ikea.com/cn/zh/catalog/categories/departments/bedroom/tools/cobe/roomset/#','http://www.ikea.com/cn/zh/catalog/categories/departments/living_room/roomset/','http://www.ikea.com/cn/zh/catalog/categories/departments/metod_kitchen/designideas/','http://www.ikea.com/cn/zh/catalog/categories/departments/dining/tools/codi/roomset/']
category=['bedroom','living','kitchen','dining']
for i in range(4):
    spider_url=url[i]
    type=category[i]
    gallery_spider(spider_url,type)