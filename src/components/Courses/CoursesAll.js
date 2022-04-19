import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { ListGroup, Row, Col, Button } from 'react-bootstrap';
import { Context } from '../../index';
import { Divider, Avatar } from "antd";
import history from "../../services/history";
import { isAdmin } from '../utils/testing';
import CreateCourse from '../Course/ModalForms/CreateCourse';
import { COURSE_INFO_ROUTE } from '../../utils/consts';

const CoursesAll = (props) => {
    const [isCreateCourseFormVisible, setIsCreateCourseFormVisible] = useState(false)
    const {userStore} = useContext(Context)
    //const data = userStore.User[5].data;
    const myCourses = userStore.MyCourses
    const allCourses = userStore.AllCourses
    const user = userStore.User;

    const handleCourse = (item) => {
        userStore.setCurCourse(item);
        history.push(COURSE_INFO_ROUTE);
    }

    const handleCreateCourse = () => {
        setIsCreateCourseFormVisible(true)
    }

    const handleSubscribeCourse = (item) => {
        userStore.setMyCourses(item);
    }

    const handleDeleteCourse = (item) => {
        userStore.deleteMyCourse(item);
        console.log(userStore.MyCourses)
    }

    const isSubscribe = (item) => {
        const courses = myCourses.filter(elem => elem.id === item.id)
        return courses.length > 0 ? true : false
    }

    const listItems = allCourses.map((item) => {
        const isSubscr = isSubscribe(item)
        //console.log(isSubscr, item)
        return (
            <ListGroup.Item 
                as="li"
                className="d-flex justify-content-between align-items-start"
                key={item.title}
            >
                <Col xs={1}>
                    <Avatar src={item.avatar} style={{marginRight: "20px"}}/>                 
                </Col>
                <Col style={{cursor: 'pointer'}} onClick={() => handleCourse(item)} xs={9}>
                    <div className="ms-2 me-auto">
                        <div className="fw-bold">{item.title}</div>
                        {item.description}
                    </div>
                </Col>
                <Col>
                    { isSubscr
                        ? <Button onClick={() => handleDeleteCourse(item)} variant="outline-danger">Покинуть курс</Button>
                        : <Button onClick={() => handleSubscribeCourse(item)} variant="outline-secondary">Подписаться</Button>
                    }
                </Col>                 
            </ListGroup.Item>
        )
    })
  
    return (
        <>
            <Row>
                <Col xs={7}>
                    <Divider orientation="left">Мои курсы:</Divider>
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

export default CoursesAll;