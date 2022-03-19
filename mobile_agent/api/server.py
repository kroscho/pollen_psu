from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
import json
import os, sys

path_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(path_dir)


from services.spqrqlQueries.main import SparqlQueries
from src.utils import typeData

app = Flask(__name__)
CORS(app)

@app.get('/api/pollen/books_by_name')
def api_get_books_by_name():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByNames(_title, typeData.Books, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/article_by_name')
def api_get_article_by_name():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByNames(_title, typeData.Articles, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/sites_by_name')
def api_get_sites_by_name():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByNames(_title, typeData.Sites, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/authors_by_name')
def api_get_authors_by_name():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getAuthorByNames(_title, typeData.Authors, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/books_by_theme')
def api_get_books_by_theme():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByTheme(_title, typeData.Books, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/article_by_theme')
def api_get_article_by_theme():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByTheme(_title, typeData.Articles, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/sites_by_theme')
def api_get_sites_by_theme():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByTheme(_title, typeData.Sites, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/authors_by_theme')
def api_get_authors_by_theme():
    _title = request.args.get('_title', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_title, _page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByTheme(_title, typeData.Authors, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/data_by_date')
def api_get_data_by_date():
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByData(_page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/article_by_date_published')
def api_get_article_by_date_published():
    _year = request.args.get('_year', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByDatePublished(int(_year), typeData.Articles, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/books_by_date_published')
def api_get_books_by_date_published():
    _year = request.args.get('_year', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByDatePublished(int(_year), typeData.Books, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response

@app.get('/api/pollen/web_by_date_published')
def api_get_web_by_date_published():
    _year = request.args.get('_year', '').replace(' ', '_')
    _page = request.args.get('_page', '').replace(' ', '_')
    _limit = request.args.get('_limit', '').replace(' ', '_')
    print(_page, _limit)
    ont = SparqlQueries()
    data, total_count = ont.getDataByDatePublished(int(_year), typeData.Sites, _page, _limit)
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
        'x-total-count': total_count
    })), 200
    print(response)
    return response




app.env = 'development'

app.run(port=5000, host='0.0.0.0', debug=True)