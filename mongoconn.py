#import lib pymongo, pip jika tidak ada
import pymongo 
#import lib time
import time
#import lib shortuuid untuk uuid random
import shortuuid
#setup connection ke mongodb
client = pymongo.MongoClient("mongodb+srv://Admin:Author@cluster0.ruhhbnu.mongodb.net/?retryWrites=true&w=majority")
DB = client["ANPR"]['Data']

#fungsi add data ke mongodb
def insert(fd,plat):
    #uuid sebagai identifier
    uuid = str(shortuuid.ShortUUID().random(length=22))
    json = {
        "uuid":uuid,
        #waktu penambahan data
        "date":str(time.strftime("%d")),
        "month":str(time.strftime("%b")),
        "year":str(time.strftime("%Y")),
        #source image raw dan edited, biasanya dipakai seperti
        # url = https://loc.com + data['raw_img]
        "raw_img":f"/static/upload/{fd}/images.jpg",
        "ocr_img":f"/static/upload/{fd}/image.jpg",
        #hasil ocr
        "ocr_result":plat
    }
    #tambah 1 data
    DB.insert_one(json)
    return uuid

#fungsi mencari database
def search(uuid):
    #mencari data dari database berdasarkan uuid yang akan langsung dikembalikan dalam bentuk JSON
    return DB.find_one({"uuid":uuid})