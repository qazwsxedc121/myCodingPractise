from bottle import Bottle, run

app = Bottle()

@app.get('/')
@app.route('/hello/<name>')
def hello(name="sdf"):
	return "Hello "+name

run(app,host="localhost", port=8080)