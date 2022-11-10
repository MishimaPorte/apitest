from sanic import Sanic
from sanic.response import json

from models import Article, ArticleIndex

from elasticsearch_dsl.query import Match

app = Sanic.get_app("main")

@app.route("/search")
async def search(request):

    #Search endpoint. Retrieves text query arg, if any, and performs index lookup to get ids.
    #Then retrieves documents from Postgres by these ids.

    arg = request.args.get("text", None)
    if arg == None or not isinstance(arg, str):
        return json({"error": "blank request"}, status = 400)
    s = ArticleIndex.search()
    s.query = Match(text = arg)
    ids = [i.meta.id for i in s.execute()]
    arts = await Article.filter(id__in=ids).order_by("created_date")
    return json([{"id": i.id, "text": i.text, "rubrics": i.rubrics, "created_date": i.created_date.isoformat()} for i in arts[0:20]], ensure_ascii = False)

@app.route("/delete/<id:int>", methods = ["POST", ])
async def delete(request, id):
    
    #Delete endpoint. Deletes an object by id provided in path.

    art = await Article.get_or_none(id = id)
    if art != None:
        await art.delete()
        s = ArticleIndex.get(id = id)
        s.delete()
        return json({"id": id})
    else:
        return json({"error": "nonexistent document"}, status = 404)
