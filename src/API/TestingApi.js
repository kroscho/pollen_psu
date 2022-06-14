import axios from "axios";

export default class TestingApi {
    static async getTests() {
        const response = await axios.get('http://localhost:5000/api/get_tests')
        return response.data
    }

    static async getTest(testName) {
        console.log("testName: ", testName)
        const response = await axios.get('http://localhost:5000/api/get_test', {
            params: {
                _testName: testName,
            }
        })
        return response.data
    }

    static async getTestWithAnswers(testName) {
        console.log("testName: ", testName)
        const response = await axios.get('http://localhost:5000/api/get_test_with_answers', {
            params: {
                _testName: testName,
            }
        })
        return response.data
    }

    static async getTest(testName) {
        console.log("testName: ", testName)
        const response = await axios.get('http://localhost:5000/api/get_test', {
            params: {
                _testName: testName,
            }
        })
        return response.data
    }

    static async createTest(item) {
        console.log("test and module: ", item.test, item.module)
        const response = await axios.post('http://localhost:5000/api/create_test', { item })
        return response.data
    }

    static async CreateSubjectArea(item) {
        const response = await axios.post('http://localhost:5000/api/create_subject_area', { item })
        return response.data
    }

    static async CreateTerm(item) {
        const response = await axios.post('http://localhost:5000/api/create_term', { item })
        return response.data
    }

    static async DeleteLecture(item) {
        const response = await axios.post('http://localhost:5000/api/delete_lecture', { item })
        return response.data
    }

    static async CreateLecture(item) {
        const response = await axios.post('http://localhost:5000/api/create_lecture', { item })
        return response.data
    }

    static async DowloadFile() {
        const response = await axios.get('http://localhost:5000/api/dowload_file')
        return response
    }

    static async DeleteTerm(item) {
        const response = await axios.post('http://localhost:5000/api/delete_term', { item })
        return response.data
    }

    static async updateTest(updatedTest) {
        console.log("updatedTest: ", updatedTest)
        const response = await axios.post('http://localhost:5000/api/update_test', { updatedTest })
        return response.data
    }

    static async deleteTest(deletedTest) {
        console.log("deletedTest: ", deletedTest)
        const response = await axios.post('http://localhost:5000/api/delete_test', { deletedTest })
        return response.data
    }

    static async deleteModule(item) {
        console.log("item: ", item)
        const response = await axios.post('http://localhost:5000/api/delete_module', { item })
        return response.data
    }

    static async deleteCourse(course) {
        console.log("deletedCourse: ", course)
        const response = await axios.post('http://localhost:5000/api/delete_course', { course })
        return response.data
    }

    static async getResultAttempt(answers, user) {
        console.log("answers: ", answers)
        console.log("user", user)
        const response = await axios.post('http://localhost:5000/api/get_result_attempt', { answers, user })
        return response.data
    }

    static async subscribeCourse(item) {
        console.log("item: ", item.uid, item.courseObj)
        const response = await axios.post('http://localhost:5000/api/subscribe_course', { item })
        return response.data
    }

    static async unsubscribeCourse(item) {
        console.log("item: ", item.uid, item.courseObj)
        const response = await axios.post('http://localhost:5000/api/unsubscribe_course', { item })
        return response.data
    }

    static async createUser(user) {
        console.log("user: ", user)
        const response = await axios.post('http://localhost:5000/api/create_user', { user })
        return response.data
    }

    static async getUser(uid) {
        const response = await axios.get('http://localhost:5000/api/get_user', {
            params: {
                _uid: uid,
            }
        })
        return response.data
    }

    static async getAttempts(user_uid, nameTest) {
        const response = await axios.get('http://localhost:5000/api/get_attempts', {
            params: {
                _uid: user_uid,
                _nameTest: nameTest,
            }
        })
        return response.data
    }

    static async getUsersWhoPassedTheTest(test) {
        const response = await axios.get('http://localhost:5000/api/get_users_who_passed_the_test', {
            params: {
                _testName: test.testName,
            }
        })
        return response.data
    }

    static async getAllCourses() {
        const response = await axios.get('http://localhost:5000/api/get_all_courses')
        return response.data
    }

    static async getUserCourses(user_uid) {
        const response = await axios.get('http://localhost:5000/api/get_user_courses', {
            params: {
                _uid: user_uid,
            }
        })
        return response.data
    }

    static async createCourse(createdCourse) {
        console.log("createdCourse: ", createdCourse)
        const response = await axios.post('http://localhost:5000/api/create_course', { createdCourse })
        return response.data
    }

    static async getCourseInfo(courseObj) {
        const response = await axios.get('http://localhost:5000/api/get_course_info', {
            params: {
                _courseObj: courseObj,
            }
        })
        return response.data
    }

    static async getMaterialsByLecture(lectureObj) {
        const response = await axios.get('http://localhost:5000/api/get_materials_by_lecture', {
            params: {
                _lectureObj: lectureObj,
            }
        })
        return response.data
    }

    static async createModule(item) {
        console.log("createdModule: ", item.createdModule, item.courseObj)
        const response = await axios.post('http://localhost:5000/api/create_module', { item })
        return response.data
    }

    static async editProfile(user) {
        console.log("user: ", user)
        const response = await axios.post('http://localhost:5000/api/edit_profile', { user })
        return response.data
    }

    static async getUsers() {
        const response = await axios.get('http://localhost:5000/api/get_users')
        return response.data
    }

    static async editRole(user) {
        console.log("user: ", user)
        const response = await axios.post('http://localhost:5000/api/edit_role', { user })
        return response.data
    }

    static async editAttempt(attempt) {
        console.log("attempt: ", attempt)
        const response = await axios.post('http://localhost:5000/api/edit_attempt', { attempt })
        return response.data
    }

    static async editModule(module) {
        console.log("module: ", module)
        const response = await axios.post('http://localhost:5000/api/edit_module', { module })
        return response.data
    }

    static async getTermsByUser(userObj, uid) {
        const response = await axios.get('http://localhost:5000/api/get_terms_by_user', {
            params: {
                _userObj: userObj,
                _uid: uid,
            }
        })
        return response.data
    }

    static async getSubjectAreas() {
        const response = await axios.get('http://localhost:5000/api/get_subject_areas')
        return response.data
    }

    static async getAnswersAuto(subjectArea, text) {
        const response = await axios.get('http://localhost:5000/api/get_answers_auto', {
            params: {
                _text: text,
                _subjectArea: subjectArea,
            }
        })
        return response.data
    }

    static async getTermsBySubjArea(subjectArea) {
        const response = await axios.get('http://localhost:5000/api/get_terms_by_subject_area', {
            params: {
                _subjectArea: subjectArea,
            }
        })
        return response.data
    }
}