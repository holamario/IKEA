from pymongo import MongoClient as mc
client=mc()
db=client.IKEA
gallery_gadget=db.GalleryGadget

gadgets=gallery_gadget.find({},{'gadgetid':1,'_id':0})
for each in gadgets:
    print(each)