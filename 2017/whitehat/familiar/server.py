from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route('/<path:path>')
def letsgo(path):
	return send_from_directory('./', 'convert.xml')
