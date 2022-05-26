import axios from "axios";

export default class TestingApi {
    static async getTests() {
        const response = await axios.get('http://localhost:5000/api/get_tests')
        return response.data
    }

    static async getTest(testName) {
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

    static async createTest(createdTest) {
        console.log("createdTest: ", createdTest)
        const response = await axios.post('http://localhost:5000/api/create_test', { createdTest })
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
}