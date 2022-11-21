
from twitter_webscript import trending_toppic
from models import tt_twitter

db=tt_twitter()

trending_toppic_list=trending_toppic()

for trending in trending_toppic_list:
    db.insert(item=trending)

from twitter_webscript import trending_toppic
from models import tt_twitter
from time import sleep

for i in range(120):
    db=tt_twitter()

    trending_toppic_list=trending_toppic()

    for trending in trending_toppic_list:
        db.insert(item=trending)

    for item in db.read():
        print (item)
    i=+1
    sleep(30)

