from bottle import route, run, template

@route('/')
def index():
    return 'Hallo'

run(host='localhost', port = 8080, reloader = True)

