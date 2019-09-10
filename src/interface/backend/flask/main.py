import flask
from flask import Flask, request, render_template, make_response
from tools import get_resource_usage, get_configuration

app = Flask(__name__)

@app.route("/manage/resource/query")
def query():
    data = get_resource_usage()
    return make_response(data)

@app.route("/manage/resource/configuration")
def configuration():
    data = get_configuration()
    return make_response(data)