import React, {useState, useContext, useEffect} from 'react';
import {InputGroup} from 'react-bootstrap';
import { Context } from '../../index';
import Pagination from '../../components/UI/Pagination/Pagination';
import './Search.css';
import Loader from '../../components/UI/Loader/Loader';
import { useFetching } from '../../components/hooks/useFetching';
import { getNumberSearchPage, getPageCount } from '../../components/utils/pages';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import Tooltip from 'react-bootstrap/Tooltip';
import { cardsItems, getResponse, getTitlePage, getTypeSearchChangeName, getTypeSearchChangeTheme, listThemes, TypeSearch, listResources } from './utils';


const Search = () => {

    const [resource, setResource] = useState(2);
    const [themes, setThemes] = useState(1);
    const [searchValue, setSearchValue] = useState("");
    const {services} = useContext(Context)
    const [totalPages, setTotalPages] = useState(0)
    const [limit, setLimit] = useState(10)
    const [page, setPage] = useState(1)
    const [data, setData] = useState([])
    const [click, setClick] = useState(true)
    const [typeSearch, setTypeSearch] = useState(TypeSearch.Default)
    const [totalCountItems, setTotalCountItems] = useState(0)
    const [searchPages, setSearchPages] = useState([])

    const [fetchItems, isDataLoading, itemsError] = useFetching(async () => {
        console.log("items: ", services.Items)
        if (searchPages.indexOf(getNumberSearchPage(page)) == -1) {
            let response = await getResponse(typeSearch, limit, getNumberSearchPage(page), searchValue, themes, services)
            setSearchPages(getNumberSearchPage(page))
            console.log("resp: ", response)
            //setData(response.data);
            setSearchPages(searchPages.concat(getNumberSearchPage(page)))
            services.setItems(response.data)
            setData(services.Items.slice((page-1)*limit, page*limit))
            setTotalCountItems(response['x-total-count'])
            setTotalPages(getPageCount(response['x-total-count'], limit))
        }
        else {
            setData(services.Items.slice((page-1)*limit, page*limit))
        }
    })

    const changeTypeSearchName = (e) => {
        e.preventDefault()
        setPage(1)
        setSearchPages([])
        services.setItems([])
        setClick(!click)
        setTypeSearch(getTypeSearchChangeName(resource))
    }

    const changeTypeSearchTheme = (e) => {
        e.preventDefault()
        setPage(1)
        services.setItems([])
        setSearchPages([])
        setClick(!click)
        setTypeSearch(getTypeSearchChangeTheme(resource))
    }

    const changePage = (p) => {
        setPage(p)
    }

    useEffect(() => {
        fetchItems()
    }, [page, click])

    return (
        <div className="contain">
            <div>
                <div className="block-left">
                    <h2>Фильтры</h2>
                    <h3>Тип ресурса</h3>
                    <select 
                        style={{width: '75%', height:'30px', border: '1px solid #000000'}}
                        value={resource} 
                        onChange={(event) => setResource(event.target.value)}
                    >
                        {listResources(services.Resources)}
                    </select>
                    <h3>Поиск по названию</h3>
                    <InputGroup className="mb-3">
                        <input
                            style={{width:'75%', height:'30px', border: '1px solid #000000'}}
                            placeholder=""
                            value={searchValue}
                            onChange={(e) => setSearchValue(e.target.value)}
                            type="text"
                        />
                        
                        <button className="st-button" onClick={changeTypeSearchName}>Найти</button>
                    </InputGroup>
                    <h3>Поиск по ключевым словам</h3>
                    <InputGroup className="mb-3">
                        <select 
                            style={{width:'75%', height:'30px', border: '1px solid #000000'}}
                            value={themes} 
                            onChange={(event) => setThemes(event.target.value)}
                        >
                            {listThemes(services.Themes)}
                        </select>
                        <button className="st-button" onClick={changeTypeSearchTheme}>Поиск</button>
                    </InputGroup>
                    <h3>Поиск по дате</h3>
                    <OverlayTrigger
                        placement='right'
                        overlay={
                            <Tooltip id={`tooltip-right`}>
                            Покажутся данные, добавленные не раньше выбранной даты.
                            </Tooltip>
                        }
                        >
                        <label for="inputDate" style={{textDecoration:'underline dotted #000000'}}>Подробнее:</label>
                    </OverlayTrigger>
                    <InputGroup className="mb-3" style={{margin: '10px 0'}}>
                        <input type="date" className="form-control" style={{height: '30px'}}></input>
                        <button className="st-button">Поиск</button>
                    </InputGroup>
                    <h3>Поиск по вашим интересам</h3>
                    <InputGroup className="mb-3">                        
                        <button className="st-button">Показать</button>
                    </InputGroup>
                </div>
                <div className="block-right">
                    {isDataLoading
                        ?<h2></h2>
                        :<h2>{getTitlePage(searchValue, resource, page, totalCountItems, typeSearch, totalPages, services.Resources)}</h2>
                    }
                    {isDataLoading 
                        ? <div style={{display:'flex', justifyContent:'center'}}><Loader></Loader></div>
                        : data
                            ? cardsItems(data)
                            :  <div style={{display:'flex', justifyContent:'center'}}>Данные не найдены</div>
                        
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