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
        ]
        this._cartAmount = 0
        makeAutoObservable(this)
    }

    setIsAuth(bool) {
        this._isAuth = bool
    }
    setUser(user) {
        this._user = user
    }

    get isAuth() {
        return this._isAuth
    }
    get User() {
        return this._user
    }

}