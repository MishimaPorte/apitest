from tortoise.models import Model
from tortoise import fields as f

from elasticsearch_dsl import Document, Text

class Article(Model):

    #Article model for postgres database.

    text = f.TextField()
    rubrics = f.JSONField()
    created_date = f.DateField(auto_now_add = True)

class ArticleIndex(Document):

    #Elastic document.

    text = Text()

    class Index:
        name = "art-index"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}
