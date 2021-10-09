import React, {useState, useContext, useEffect} from 'react';
import {InputGroup, Button, FormControl, Dropdown, DropdownButton} from 'react-bootstrap';
import { Context } from '../../index';
import CardItem from '../../components/Card/Card'
import Pagination from '../../components/UI/Pagination/Pagination';
import './Search.css';
import axios from 'axios';
import ItemService from '../../API/ItemService';
import Loader from '../../components/UI/Loader/Loader';
import { useFetching } from '../../components/hooks/useFetching';
import { getPageCount } from '../../components/utils/pages';


const Search = () => {

    const [resource, setResource] = useState(5);
    const [themes, setThemes] = useState(1);
    const [searchValue, setSearchValue] = useState("");
    const {services} = useContext(Context)
    const [totalPages, setTotalPages] = useState(0)
    const [limit, setLimit] = useState(10)
    const [page, setPage] = useState(1)
    const [data, setData] = useState([])
    

    const [fetchItems, isDataLoading, itemsError] = useFetching(async () => {
        const response = await ItemService.getAll(limit, page);
        setData(response.data);
        const totalCount = response.headers['x-total-count']
        setTotalPages(getPageCount(totalCount, limit))
    })

    const listThemes = services.Themes.map((item) => {
        return (
            <option value={item.id}>{item.name}</option>
        )
    })

    const cardsItems = data.map((item) => {
        return (
            <CardItem data={item}></CardItem>
        )
    })

    const changePage = (p) => {
        setPage(p)
    }

    useEffect(() => {
        fetchItems()
    }, [page])

    return (
        <div className="contain">
            <div>
                <div className="block-left">
                    <h2>Фильтры</h2>
                    <h3>Тип ресурса</h3>
                    <select 
                        style={{width:'75%', height:'30px', border: '1px solid #000000'}}
                        value={resource} 
                        onChange={(event) => setResource(event.target.value)}
                    >
                        <option value="1">Книги</option>
                        <option value="2">Статьи</option>
                        <option value="3">Сайты</option>
                        <option value="4">Авторы</option>
                        <option value="5">Все</option>
                    </select>
                    <h3>Поиск по названию</h3>
                    <InputGroup className="mb-3">
                        <input
                            style={{width:'75%', height:'30px', border: '1px solid #000000'}}
                            placeholder="Search..."
                            value={searchValue}
                            onChange={(e) => setSearchValue(e.target.value)}
                            type="text"
                        />
                        
                        <button className="st-button">Найти</button>
                    </InputGroup>
                    <h3>Поиск по ключевым словам</h3>
                    <InputGroup className="mb-3">
                        <select 
                            style={{width:'75%', height:'30px', border: '1px solid #000000'}}
                            value={themes} 
                            onChange={(event) => setThemes(event.target.value)}
                        >
                            {listThemes}
                        </select>
                        <button className="st-button">Поиск</button>
                    </InputGroup>
                    <h3>Поиск по дате</h3>
                </div>
                <div className="block-right">
                    <h2>Актуальные данные за 3 дня</h2>
                    {isDataLoading 
                        ? <div style={{display:'flex', justifyContent:'center'}}><Loader></Loader></div>
                        : cardsItems
                    }
                    {isDataLoading
                        ? <div></div>
                        : <Pagination 
                            totalPages={totalPages} 
                            changePage={changePage} 
                            page={page}
                        ></Pagination>
                    }
                </div>
            </div>
        </div>
    )
}

export default Search;