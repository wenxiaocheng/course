import pymongo
from course import settings

host = settings.MONGODB_HOST
port = settings.MONGODB_PORT
db_name = settings.MONGODB_DBNAME
client = pymongo.MongoClient(host=host, port=port)
tdb = client[db_name]
post = tdb[settings.MONGODB_DOCNAME]

key_word = '定向爬虫'
course = post.find({'title': {'$regex': '.*((?i){}).*'.format(key_word)}})
print('共找到了{}门课程'.format(course.count()))
for each in course:
    print(each['title'],each['link'])
