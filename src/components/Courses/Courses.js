import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { ListGroup, Row, Col, Button } from 'react-bootstrap';
import { Context } from '../../index';
import { Divider, Avatar } from "antd";
import history from "../../services/history";
import { isAdmin } from '../utils/testing';
import CreateCourse from '../Course/ModalForms/CreateCourse';
import { COURSE_INFO_ROUTE, TESTING_ALL_COURSES_ROUTE } from '../../utils/consts';

const Courses = (props) => {
    const [isCreateCourseFormVisible, setIsCreateCourseFormVisible] = useState(false)
    const {userStore} = useContext(Context)
    //const data = userStore.User[5].data;
    
    const data = userStore.MyCourses
    const user = userStore.User;

    const handleCourse = (item) => {
        userStore.setCurCourse(item);
        history.push(COURSE_INFO_ROUTE);
    }

    const handleAddCourse = () => {
        history.push(TESTING_ALL_COURSES_ROUTE);
    }

    const handleCreateCourse = () => {
        setIsCreateCourseFormVisible(true)
    }

    if (history.action === "POP") {
        console.log("POPOPO")
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
                    <Button onClick={handleAddCourse} variant="outline-success">Добавить</Button>{' '}
                </Col>
                { isAdmin(user)
                    ? <Col><Button onClick={handleCreateCourse} style={{marginLeft: "5px"}} variant="outline-success">Создать курс</Button></Col>
                    : null
                }
            </Row>
            <CreateCourse isVisible={isCreateCourseFormVisible} setIsVisible={setIsCreateCourseFormVisible}></CreateCourse>
            <ListGroup variant="flush">
                {listItems}
            </ListGroup>    
        </>
    )
}

export default Courses;