import React, {useState, useContext, useEffect} from 'react';
import ItemService from '../../API/ItemService';
import CardItem from '../../components/Card/Card';

export const TypeSearch = { 
    BooksByName: 1, 
    ArticleByName: 2, 
    WebByName: 3, 
    BooksByTheme: 4, 
    ArticleByTheme: 5, 
    WebByTheme: 6, 
    AuthorByName: 7, 
    AuthorByTheme: 8, 
    AllByName: 9, 
    AllByTheme: 10, 
    Default:11 
};

export const getResponse = async (typeSearch, limit, page, searchValue, themes, services) => {

    let response;
    switch (typeSearch) {
        case TypeSearch.BooksByName:
            response = await ItemService.getBooksByName(limit, page, searchValue);
            break;
        case TypeSearch.ArticleByName:
            response = await ItemService.getArticlesByName(limit, page, searchValue);
            break;
        case TypeSearch.WebByName:
            response = await ItemService.getSitesByName(limit, page, searchValue); 
            break;
        case TypeSearch.AuthorByName:
            response = await ItemService.getAuthorsByName(limit, page, searchValue);       
            break;
        case TypeSearch.BooksByTheme:
            response = await ItemService.getBooksByTheme(limit, page, services.Themes[themes-1].name);
            break;
        case TypeSearch.ArticleByTheme:
            response = await ItemService.getArticlesByTheme(limit, page, services.Themes[themes-1].name);
            break;
        case TypeSearch.WebByTheme:
            response = await ItemService.getSitesByTheme(limit, page, services.Themes[themes-1].name); 
            break;
        case TypeSearch.AuthorByTheme:
            response = await ItemService.getAuthorsByTheme(limit, page, services.Themes[themes-1].name);       
            break;
        default:
            response = await ItemService.getArticlesByName(limit, page, services.Themes[themes-1].name);
    }
    return response;
}



export const getTitlePage = (searchValue, resourse, page, total, typeSearch, totalPages, themes) => {
    console.log("themes: ", themes)
    let resourceText;
    themes.forEach((elem) => {
        if (elem.id === resourse.toString()) {
            resourceText = elem.name;
            return;
        }
    })
    console.log("resText: ", resourceText)
    let text;
    if (typeSearch != TypeSearch.Default) {
        text = `Результаты поиска по запросу <<${searchValue}>>, ${resourceText}. \nСтраница: ${page}, Всего страниц: ${totalPages}, Всего найдено: ${total}`
    }
    else {
        text = `Актуальные данные за последние 3 дня. Всего страниц: ${totalPages}, Всего найдено: ${total}`
    }
    return text;
}

export const getTypeSearchChangeName = (resource) => {
    switch (resource) {
        case "1": 
            return TypeSearch.BooksByName;
        case "2":
            return TypeSearch.ArticleByName;
        case "3":
            return TypeSearch.WebByName;
        case "4":
            return TypeSearch.AuthorByName;
        case "5": 
            return TypeSearch.AllByName;
        default:
            return TypeSearch.ArticleByName;
    }
}

export const getTypeSearchChangeTheme = (resource) => {
    switch (resource) {
        case "1": 
            return TypeSearch.BooksByTheme;
        case "2":
            return TypeSearch.ArticleByTheme;
        case "3":
            return TypeSearch.WebByTheme;
        case "4":
            return TypeSearch.AuthorByTheme;
        case "5": 
            return TypeSearch.AllByTheme;
        default:
            return TypeSearch.ArticleByTheme;
    }
}

export const listThemes = (themes) => themes.map((item) => {
    return (
        <option value={item.id} key={item.id}>{item.name}</option>
    )
})

export const listResources = (resources) => resources.map((item) => {
    return (
        <option value={item.id} key={item.id}>{item.name}</option>
    )
})

export const cardsItems = (data) => data.map((item, index) => {
    return (
        <CardItem data={item} key={index}></CardItem>
    )
})