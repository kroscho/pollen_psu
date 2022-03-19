import {makeAutoObservable} from 'mobx';

export default class UserStore {
    constructor() {
        this._isAuth = false
        this._user = [
            {id: "Имя", data: "Nikita Grishin"},
            {id: "Возраст", data: 21},
            {id: "Почта", data: "kros@mail.ru"},
            {id: "Роль", data: "admin"},
            {id: "Интересы", data: ["theme1", "theme2", "theme3"]},
            {id: "Курсы", data: [
                {
                    title: "Курс1", 
                    avatar: "https://joeschmoe.io/api/v1/random", 
                    description: "Описание первого курса", 
                    info: "Большая информация об этом курсе имеено в этом тексте предоставлена. Цель курса обеспечить студентов знаниями и не только. Жить в кайф надо, а не вот это вот все.",
                    students: [
                        {id: "1", name: "Kurs1 Student1", url: "https://joeschmoe.io/api/v1/random"},
                        {id: "2", name: "Kurs2 Student2", url: "https://joeschmoe.io/api/v1/random"},
                        {id: "3", name: "Kurs3 Student3", url: "https://joeschmoe.io/api/v1/random"},
                    ],
                    tests: [
                        {
                            id: "1", 
                            attempts: 0,
                            name: "Тест 1. Название",
                            variants: [
                                {
                                    id: "1",
                                    name: "Вариант 1",
                                    tasks: [
                                        {
                                            id: "1",
                                            type: "single",
                                            question: "Вопрос 1",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "2",
                                            type: "multiple",
                                            question: "Вопрос 2",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "3",
                                            type: "truefalse",
                                            question: "Вопрос 3",
                                            answers: [
                                                {id: "1", answer: "Да"},
                                                {id: "2", answer: "Нет"},
                                            ]
                                        },
                                        {
                                            id: "4",
                                            type: "text",
                                            question: "Вопрос 4",
                                            answers: [],
                                        },
                                    ]
                                },
                                {
                                    id: "2",
                                    name: "Вариант 2",
                                    tasks: [
                                        {
                                            id: "1",
                                            type: "multiple",
                                            question: "Вопрос 1",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "2",
                                            type: "single",
                                            question: "Вопрос 2",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "3",
                                            type: "truefalse",
                                            question: "Вопрос 3",
                                            answers: [
                                                {id: "1", answer: "Да"},
                                                {id: "2", answer: "Нет"},
                                            ]
                                        },
                                        {
                                            id: "4",
                                            type: "text",
                                            question: "Вопрос 4",
                                            answers: [],
                                        },
                                    ]
                                }
                            ]
                        },
                        {
                            id: "2", 
                            attempts: 2,
                            name: "Тест 2. Название",
                            variants: [
                                {
                                    id: "1",
                                    name: "Вариант 1",
                                    tasks: [
                                        {
                                            id: "1",
                                            type: "single",
                                            question: "Вопрос 1",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "2",
                                            type: "multiple",
                                            question: "Вопрос 2",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "3",
                                            type: "truefalse",
                                            question: "Вопрос 3",
                                            answers: [
                                                {id: "1", answer: "Да"},
                                                {id: "2", answer: "Нет"},
                                            ]
                                        },
                                        {
                                            id: "4",
                                            type: "text",
                                            question: "Вопрос 4",
                                            answers: [],
                                        },
                                    ]
                                },
                                {
                                    id: "2",
                                    name: "Вариант 2",
                                    tasks: [
                                        {
                                            id: "1",
                                            type: "multiple",
                                            question: "Вопрос 1",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "2",
                                            type: "single",
                                            question: "Вопрос 2",
                                            answers: [
                                                {id: "1", answer: "Ответ 1"},
                                                {id: "2", answer: "Ответ 2"},
                                                {id: "3", answer: "Ответ 3"},
                                                {id: "4", answer: "Ответ 4"},
                                            ]
                                        },
                                        {
                                            id: "3",
                                            type: "truefalse",
                                            question: "Вопрос 3",
                                            answers: [
                                                {id: "1", answer: "Да"},
                                                {id: "2", answer: "Нет"},
                                            ]
                                        },
                                        {
                                            id: "4",
                                            type: "text",
                                            question: "Вопрос 4",
                                            answers: [],
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    title: "Курс2", 
                    avatar: "https://joeschmoe.io/api/v1/random", 
                    description: "Описание второго курса", 
                    info: "Большая информация об этом курсе имеено в этом тексте предоставлена. Цель курса обеспечить студентов знаниями и не только. Жить в кайф надо, а не вот это вот все.",
                    students: [
                        {id: "1", name: "Kurs2 Student1", url: "https://joeschmoe.io/api/v1/random"},
                        {id: "2", name: "Kurs2 Student2", url: "https://joeschmoe.io/api/v1/random"},
                    ],
                    tests: [],
                },
                {
                    title: "Курс3", 
                    avatar: "https://joeschmoe.io/api/v1/random", 
                    description: "Описание третьего курса", 
                    info: "Большая информация об этом курсе имеено в этом тексте предоставлена. Цель курса обеспечить студентов знаниями и не только. Жить в кайф надо, а не вот это вот все.",
                    students: [
                        {id: "1", name: "Kurs3 Student1", url: "https://joeschmoe.io/api/v1/random"},
                        {id: "2", name: "Kurs3 Student2", url: "https://joeschmoe.io/api/v1/random"},
                        {id: "3", name: "Kurs3 Student3", url: "https://joeschmoe.io/api/v1/random"},
                    ],
                    tests: [],
                }
            ]}
        ]
        this._curCourse = {}
        this._curTest = {}
        this._curVariant = {}
        this._cartAmount = 0
        makeAutoObservable(this)
    }

    setIsAuth(bool) {
        this._isAuth = bool
    }
    setUser(user) {
        this._user = user
    }

    setCurCourse(item) {
        this._curCourse = item
    }

    setCurTest(item) {
        this._curTest = item
    }

    setCurVariant(item) {
        this._curVariant = item
    }

    get isAuth() {
        return this._isAuth
    }
    get User() {
        return this._user
    }

    get CurCourse() {
        return this._curCourse
    }

    get CurTest() {
        return this._curTest
    }

    get CurVariant() {
        return this._curVariant
    }

}