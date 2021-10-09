import React from 'react';

import './Card.css';

const CardItem = ({data}) => {
    return (
        <div className="card">
            <h3>{data?.title}</h3>
            <span> <b>Авторы:</b> {data?.title}</span> 
            <span><b>Ключевые слова:</b> {data?.title}</span>
            <a href={data?.url}>Подробнее</a>
        </div>
    )
}

export default CardItem;