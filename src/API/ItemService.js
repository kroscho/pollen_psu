import axios from "axios";

export default class ItemService {
    static async getAll(limit=10, page=1) {
        const response = await axios.get('https://jsonplaceholder.typicode.com/photos', {
            params: {
                _limit: limit,
                _page: page
            }
        })
        return response
    }

    static async getBooksByName(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/books_by_name', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getArticlesByName(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/article_by_name', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getSitesByName(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/sites_by_name', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getAuthorsByName(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/authors_by_name', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getBooksByTheme(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/books_by_theme', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getArticlesByTheme(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/article_by_theme', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getSitesByTheme(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/sites_by_theme', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

    static async getAuthorsByTheme(limit=10, page=1, title="") {
        const response = await axios.get('http://localhost:5000/api/pollen/authors_by_theme', {
            params: {
                _limit: limit,
                _page: page,
                _title: title
            }
        })
        console.log("response: ", response.data.data)
        return response.data
    }

}