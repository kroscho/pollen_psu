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

path_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(path_dir)

from testing.sparqlQueries.main import TestingService

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

@app.post('/api/create_test')
def api_create_test():
    _newTest = request.get_json()
    print("New test: ", _newTest['createdTest'])
    _newTest = _newTest['createdTest']
    ont = TestingService()
    isExistNameTest = ont.checkNameTest(testName=_newTest['nameTest'])
    if isExistNameTest:
        return make_response(json.dumps({
            'statusCode': 422,
            'error': 'Тест с таким названием уже существует'
        })), 422
    ont.createTest(_newTest)
    return make_response(json.dumps({
        'statusCode': 200,
        'data': "Тест успешно создан",
    })), 200

@app.get('/api/get_tests')
def api_get_tests():
    ont = TestingService()
    data = ont.getTests()
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_test_with_answers')
def api_get_test_with_answers():
    ont = TestingService()
    _testName = request.args.get('_testName', '').replace(' ', '_')
    print("NAME: ", _testName)
    data = ont.getTestWithAnswers(_testName)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.post('/api/update_test')
def api_update_test():
    ont = TestingService()
    _updatedTest = request.get_json()
    print("Updated test: ", _updatedTest.get('updatedTest'))
    _updatedTest = _updatedTest.get('updatedTest')
    print("Upd Name: ", _updatedTest.get('nameTest'))
    ont.updateTest(_updatedTest)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print("response: ", response)
    return response

@app.post('/api/delete_test')
def api_delete_test():
    ont = TestingService()
    _deletedTest = request.get_json()
    print("Deleted test: ", _deletedTest.get('deletedTest'))
    _deletedTest = _deletedTest.get('deletedTest')
    print("Del Name: ", _deletedTest.get('nameTest'))
    ont.deleteTest(_deletedTest)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print("response: ", response)
    return response

app.env = 'development'

app.run(port=5000, host='0.0.0.0', debug=True)