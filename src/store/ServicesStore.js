import {makeAutoObservable} from 'mobx';

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
}