import {makeAutoObservable} from 'mobx';
import { ADD_ROUTE, ALLERGENS_ROUTE, COURSE_TESTS_TEST_ROUTE, COURSE_TESTS_TEST_VARIANTS_ROUTE, ARCHIVE_ROUTE, COURSE_INFO_ROUTE, COURSE_LECTIONS_ROUTE, COURSE_LITERATURE_ROUTE, COURSE_TESTS_ROUTE, MAIN_ROUTE, PROFILE_ROUTE, SEARCH_ROUTE, TESTING_ALL_COURSES_ROUTE, TESTING_COURSES_ROUTE, TESTING_ROUTE, VIEW_ROUTE, COURSE_LECTURE_ROUTE, TESTING_TESTS_ROUTE, TESTING_INFO_ROUTE, TESTING_MATERIALS_ROUTE, TESTS_TEST_ROUTE, TESTS_TEST_ATTEMPT_ROUTE } from '../utils/consts';

export default class UserStore {
    constructor() {
        this._themes = [
            { id: "1", name: 'палинология' },
            { id: "2", name: 'palynology' },
            { id: "3", name: 'пыльцевые зерна' },
            { id: "4", name: 'pollen grains' },
        ]

        this._resource = [
            { id: "1", name: 'Книги' },
            { id: "2", name: 'Статьи' },
            { id: "3", name: 'Сайты' },
            { id: "4", name: 'Авторы' },
        ]

        this._menuTesting1 = [
            { id: "1", name: 'Мои курсы', link: TESTING_COURSES_ROUTE },
            { id: "2", name: 'Все курсы', link: TESTING_ALL_COURSES_ROUTE },
        ]

        this._menuTesting = [
            { id: "1", name: 'Информация', link: TESTING_INFO_ROUTE },
            { id: "2", name: 'Тесты', link: TESTING_TESTS_ROUTE },
            { id: "3", name: 'Материалы', link: TESTING_MATERIALS_ROUTE },
        ]

        this._menuCourse = [
            { id: "1", name: 'Информация', link: COURSE_INFO_ROUTE },
            { id: "2", name: 'Лекции', link: COURSE_LECTIONS_ROUTE },
            { id: "3", name: 'Тесты', link: COURSE_TESTS_ROUTE },
            { id: "4", name: 'Литература', link: COURSE_LITERATURE_ROUTE },
            { id: "5", name: 'Мои курсы', link: TESTING_COURSES_ROUTE },
            { id: "6", name: 'Все курсы', link: TESTING_ALL_COURSES_ROUTE },
        ]

        this._menuApp = [
            { id: "1", name: 'Главная', link: MAIN_ROUTE },
            { id: "2", name: 'Аллергены', link: ALLERGENS_ROUTE },
            { id: "3", name: 'Добавление', link: ADD_ROUTE },
            { id: "4", name: 'Мониторинг', link: VIEW_ROUTE },
            { id: "5", name: 'Архив', link: ARCHIVE_ROUTE },
            { id: "6", name: 'Поиск', link: SEARCH_ROUTE },
            { id: "7", name: 'Тестирование', link: TESTING_COURSES_ROUTE },
            { id: "8", name: 'Профиль', link: PROFILE_ROUTE },
        ]

        this._tests = [
            {
                id: "1", 
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

        this._routes = {
            "/testing/info": [
                {path: TESTING_INFO_ROUTE, title: "Информация", active: true},
            ],
            "/testing/tests": [
                {path: TESTING_TESTS_ROUTE, title: "Тесты", active: true},
            ],
            "/testing/materials": [
                {path: TESTING_MATERIALS_ROUTE, title: "Материалы", active: true},
            ],
            "/testing/tests/test": [
                {path: TESTING_TESTS_ROUTE, title: "Тесты", active: false},
                {path: TESTS_TEST_ROUTE, title: "Тест", active: true},
            ],
            "/testing/tests/test/attempt": [
                {path: TESTING_TESTS_ROUTE, title: "Тесты", active: false},
                {path: TESTS_TEST_ROUTE, title: "Тест", active: false},
                {path: TESTS_TEST_ATTEMPT_ROUTE, title: "Попытка", active: true},                
            ],
            "/course/info": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_INFO_ROUTE, title: "Информация о курсе", active: true},
            ],
            "/course/lections": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_LECTIONS_ROUTE, title: "Лекции", active: true},
            ],
            "/course/lectures/lecture": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_LECTIONS_ROUTE, title: "Лекции", active: false},
                {path: COURSE_LECTURE_ROUTE, title: "Лекция", active: true},
            ],
            "/course/tests": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_TESTS_ROUTE, title: "Тесты", active: true},
            ],
            "/course/literature": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_LITERATURE_ROUTE, title: "Литература", active: true},
            ],
            "/course/tests/test/variants": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_TESTS_ROUTE, title: "Тесты", active: false},
                {path: COURSE_TESTS_TEST_VARIANTS_ROUTE, title: "Варианты", active: true},
            ],
            "/course/tests/test": [
                {path: TESTING_COURSES_ROUTE, title: "Мои курсы", active: false}, 
                {path: COURSE_TESTS_ROUTE, title: "Тесты", active: false},
                {path: COURSE_TESTS_TEST_VARIANTS_ROUTE, title: "Варианты", active: false},
                {path: COURSE_TESTS_TEST_ROUTE, title: "Тест", active: true},
            ],
        }

        const getListYears = () => {
            let resultList = []
            let j = 1;
            for (let i = 2022; i > 1950; i--) {
                resultList.push({id: j, name: i});
                j++;
            }
            return resultList;
        }

        this._years = getListYears()

        this._items = []

        makeAutoObservable(this)
    }

    setThemes(themes) {
        this._themes = themes
    }

    setResource(resource) {
        this._resource = resource
    }

    setItems(items) {
        if (items.length != 0) {
            this._items = this._items.concat(items)
        }
        else {
            this._items = []
        }
    }

    setTests(items) {
        this._tests = items
    }

    get MenuTesting() {
        return this._menuTesting
    }

    get MenuCourse() {
        return this._menuCourse
    }

    get MenuApp() {
        return this._menuApp
    }

    get Years() {
        return this._years
    }

    get Resources() {
        return this._resource
    }

    get Themes() {
        return this._themes
    }

    get Items() {
        return this._items
    }

    get Routes() {
        return this._routes
    }

    get Tests() {
        return this._tests
    }
}