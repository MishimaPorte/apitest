import csv
from datetime import datetime
from models import Article,  ArticleIndex
import json



async def init_dbs():
    #Initializes Postgres and Elasticsearch with data from csv file.
    ArticleIndex.init()
    with open("../posts.csv") as file:
        csv_file = csv.reader(file)
        for id, row in enumerate(csv_file):
            if id == 0:
                continue
            text = row[0]
            date = datetime.fromisoformat(row[1])
            cats = json.loads(row[2].strip('"').replace("'", '"'))

            a = Article(id = id, text = text, created_date = date, rubrics = cats)
            await a.save()

            ArticleIndex(_id = id, text = text).save()
        ArticleIndex._index.refresh()
