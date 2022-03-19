import React, { useContext } from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { ListGroup, Row, Col, Button } from 'react-bootstrap';
import { Context } from '../../index';
import { Divider, Avatar } from "antd";
import history from "../../services/history";
import { isAdmin } from '../utils/testing';

const ListCourses = (props) => {
    const {userStore} = useContext(Context)
    const data = userStore.User[5].data;
    const user = userStore.User;

    const handleCourse = (item) => {
        userStore.setCurCourse(item);
        history.push("../../course/info");
    }

    const listItems = data.map((item) => {
        return (
            <ListGroup.Item 
                as="li"
                className="d-flex justify-content-between align-items-start"
                style={{cursor: 'pointer'}}
                onClick={() => handleCourse(item)}
                key={item.title}
            >
                <Avatar src={item.avatar} style={{marginRight: "20px"}}/>
                <div className="ms-2 me-auto">
                    <div className="fw-bold">{item.title}</div>
                    {item.description}
                </div>                    
            </ListGroup.Item>
        )
    })
  
    return (
        <>
            <Row>
                <Col xs={7}>
                    <Divider orientation="left">Мои курсы:</Divider>
                </Col>
                <Col>
                    <Button variant="outline-success">Добавить</Button>{' '}
                </Col>
                { isAdmin(user)
                    ? <Col><Button style={{marginLeft: "5px"}} variant="outline-success">Создать курс</Button></Col>
                    : null
                }
            </Row>
            <ListGroup variant="flush">
                {listItems}
            </ListGroup>    
        </>
    )
}

export default ListCourses;