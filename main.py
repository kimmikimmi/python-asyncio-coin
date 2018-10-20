from sanic import Sanic
from sanic.response import json
from sanic.response import text
from coin_service import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = Sanic()


@app.listener('before_server_start')
async def initialize_scheduler(app, loop):
    scheduler = AsyncIOScheduler({'event_loop': loop})

    scheduler.add_job(check_new_coin, 'interval', seconds=1, max_instances=2)
    scheduler.add_job(make_a_deal, 'interval', seconds=2, max_instances=2)

    scheduler.start()


@app.route("/json")
def post_json(request):
    return json({"received": True, "message": request.json})


@app.route("/query_srting")
def query_string(request):
    return json({"parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string})


@app.route("/files")
def post_dto(request):
    test_file = request.files.get('test')

    file_parameters = {
        'body': test_file.body,
        'name': test_file.name,
        'type': test_file.type
    }

    return json({"received": True, "file_names": request.files.key(), "test_file_parameters": file_parameters})


@app.route('/youshallnotpass')
async def no_no(request):
    abort(401)
    # this won't happen
    text('ok')


@app.route('/')
async def test(request):
    return json({"hello": "world"})


@app.route('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))


@app.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Number - {}'.format(integer_arg))


@app.route('/number/<number_arg:number>')
async def number_handler(reqeust, number_arg):
    return text('Number - {}'.format(number_arg))


@app.route('/person/<name:[A-z]+>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))


@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(reqeust, folder_id):
    return text('Folder - {}'.format(folder_id))


@app.route('/post', methods=['POST'])
async def post_handler(request):
    return text('POST request - {}'.format(request.json))


@app.route('/get', methods=['GET'])
async def get_handler(request):
    return text('GET request - {}'.foramt(request.args))


async def handler1(request):
    return text('OK')


app.add_route(handler1, '/test')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
