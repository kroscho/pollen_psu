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
    _item = request.get_json()
    _item = _item.get('item')
    print("Test And Module: ", _item["test"], _item["module"])
    test = _item["test"] 
    module = _item["module"]
    ont = TestingService()
    isExistNameTest = ont.checkNameTest(test['testName'])
    if isExistNameTest:
        return make_response(json.dumps({
            'statusCode': 422,
            'error': 'Тест с таким названием уже существует'
        })), 422
    ont.createTest(test, module)
    return make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200

@app.post('/api/create_course')
def api_create_course():
    _newCourse = request.get_json()
    print("New course: ", _newCourse['createdCourse'])
    _newCourse = _newCourse['createdCourse']
    ont = TestingService()
    isExistNameCourse = ont.checkNameCourse(_newCourse['title'])
    if isExistNameCourse:
        return make_response(json.dumps({
            'statusCode': 422,
            'error': 'Курс с таким названием уже существует'
        })), 422
    ont.createCourse(_newCourse)
    return make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200

@app.post('/api/create_module')
def api_create_module():
    _item = request.get_json()
    _item = _item.get('item')
    print("Module CourseObj: ", _item["module"], _item["courseObj"])
    ont = TestingService()
    ont.createModule(_item["module"], _item["courseObj"])
    return make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
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

@app.get('/api/get_test')
def api_get_test():
    ont = TestingService()
    _testName = request.args.get('_testName', '')
    print("NAME: ", _testName)
    data = ont.getTest(_testName)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_all_courses')
def api_get_all_courses():
    ont = TestingService()
    data = ont.getAllCourses()
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_test_with_answers')
def api_get_test_with_answers():
    ont = TestingService()
    _testName = request.args.get('_testName', '')
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
    print("Upd Name: ", _updatedTest.get('testName'))
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
    print("Del Name: ", _deletedTest.get('testName'))
    ont.deleteTest(_deletedTest)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print("response: ", response)
    return response

@app.post('/api/delete_course')
def api_delete_course():
    ont = TestingService()
    _course = request.get_json()
    print("Deleted course: ", _course.get('course'))
    _course = _course.get('course')
    print("Del Name: ", _course.get('courseObj'))
    ont.deleteCourse( _course.get('courseObj'))
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print("response: ", response)
    return response

@app.post('/api/delete_module')
def api_delete_module():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('item')
    moduleObj = _item["moduleObj"]
    courseObj = _item["courseObj"]
    print("Uid CourseObj: ", moduleObj, courseObj)
    ont.deleteModule(moduleObj, courseObj)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print("response: ", response)
    return response

@app.post('/api/get_result_attempt')
def api_get_result_attempt():
    ont = TestingService()
    _answers = request.get_json()
    _answers = _answers.get('answers')
    _user = request.get_json()
    _user = _user.get('user')
    print("Test Name: ", _answers['testName'], _user["firstName"])
    data = ont.getResultAttempt(_answers, _user)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.post('/api/create_user')
def api_create_user():
    ont = TestingService()
    _user = request.get_json()
    _user = _user.get('user')
    print("Email: ", _user['email'])
    ont.createUser(_user)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.get('/api/get_user')
def api_get_user():
    ont = TestingService()
    _uid = request.args.get('_uid', '')
    print("UiDD: ", _uid)
    data = ont.getUser(_uid)
    print("User: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_attempts')
def api_get_attempts():
    ont = TestingService()
    _uid = request.args.get('_uid', '')
    _nameTest = request.args.get('_nameTest', '')
    print("Uid TestName: ", _uid, _nameTest)
    data = ont.getAttempts(_uid, _nameTest)
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_last_attempt')
def api_get_last_attempts():
    ont = TestingService()
    _uid = request.args.get('_uid', '')
    _nameTest = request.args.get('_nameTest', '')
    print("Uid TestName: ", _uid, _nameTest)
    data = ont.getAttempts(_uid, _nameTest)
    print("data: ", data[-1])
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data[-1],
    })), 200
    print(response)
    return response 

@app.get('/api/get_user_courses')
def api_get_user_courses():
    ont = TestingService()
    _uid = request.args.get('_uid', '')
    print("Uid: ", _uid,)
    data = ont.getUserCourses(_uid)
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response    

@app.post('/api/subscribe_course')
def api_subscribe_course():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('item')
    print("Uid CourseObj: ", _item["uid"], _item["courseObj"])
    data = ont.subscribeCourse(_item["uid"], _item["courseObj"])
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.post('/api/unsubscribe_course')
def api_unsubscribe_course():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('item')
    print("Uid CourseObj: ", _item["uid"], _item["courseObj"])
    ont.unsubscribeCourse(_item["uid"], _item["courseObj"])
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.get('/api/get_course_info')
def api_get_course_info():
    ont = TestingService()
    _courseObj = request.args.get('_courseObj', '')
    print("courseObj: ", _courseObj,)
    data = ont.getCourseInfo(_courseObj)
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response 

@app.post('/api/edit_profile')
def api_edit_profile():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('user')
    print("User: ", _item)
    ont.editProfile(_item)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.get('/api/get_users')
def api_get_users():
    ont = TestingService()
    data = ont.getUsers()
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_users_who_passed_the_test')
def api_get_users_who_passed_the_test():
    ont = TestingService()
    _testName = request.args.get('_testName', '')
    print("courseObj: ", _testName,)
    data = ont.getUsersWhoPassedTheTest(_testName)
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.post('/api/edit_role')
def api_edit_role():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('user')
    print("User: ", _item)
    ont.editRole(_item)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.post('/api/edit_attempt')
def api_edit_attempt():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('attempt')
    print("Attempt: ", _item)
    ont.editAttempt(_item)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.post('/api/edit_module')
def api_edit_module():
    ont = TestingService()
    _item = request.get_json()
    _item = _item.get('module')
    print("module: ", _item)
    ont.editModule(_item)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': "ok",
    })), 200
    print(response)
    return response

@app.get('/api/get_terms_by_user')
def api_get_terms_by_user():
    ont = TestingService()
    _userObj = request.args.get('_userObj', '')
    print("userObj: ", _userObj)
    data = ont.getTermsByUser(_userObj)
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_subject_areas')
def api_get_subject_areas():
    ont = TestingService()
    data = ont.getSubjectAreas()
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

@app.get('/api/get_answers_auto')
def api_get_answers_auto():
    ont = TestingService()
    _subjectArea = request.args.get('_subjectArea', '')
    _text = request.args.get('_text', '')
    print("text, subjectArea: ", _text, _subjectArea)
    data = ont.getAnswersByTaskAuto(_text, _subjectArea)
    print("data: ", data)
    
    response = make_response(json.dumps({
        'statusCode': 200,
        'data': data,
    })), 200
    print(response)
    return response

app.env = 'development'

app.run(port=5000, host='0.0.0.0', debug=True)