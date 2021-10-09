import {makeAutoObservable} from 'mobx';

export default class UserStore {
    constructor() {
        this._themes = [
            { id: "1", name: 'Пыльцевые зерна' },
            { id: "2", name: 'Тема2' },
            { id: "3", name: 'Тема3' },
            { id: "4", name: 'Тема4' },
            { id: "5", name: 'Тема5' }
        ]


        makeAutoObservable(this)
    }

    setThemes(themes) {
        this._themes = themes
    }

    get Themes() {
        return this._themes
    }

}