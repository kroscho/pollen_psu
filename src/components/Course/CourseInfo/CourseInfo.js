import React, { useContext } from "react";
import 'antd/dist/antd.css';
import { Divider, Avatar } from "antd";
import { Context } from "../../..";
import {Row, Col, ListGroup, Button, Badge} from "react-bootstrap"
import { BookOutlined } from '@ant-design/icons';

const CourseInfo = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;

    let listStudents = []
    let listModules = []
    let countPractice = 0
    let countLectures = 0

    const handleDeleteCourse = (item) => {
        userStore.deleteMyCourse(item);
        console.log(userStore.MyCourses)
    }

    if (curCourse.students) {
        listStudents = curCourse.students.map((item) => {
            return (
                <ListGroup.Item 
                    as="li"
                    className="d-flex justify-content-between align-items-start"
                    key={item.id}
                >
                    <Avatar src={item.url} style={{marginRight: "20px"}}/>
                    <div className="ms-2 me-auto">
                        {item.name}
                    </div>                    
                </ListGroup.Item>
            )
        })
    }

    if (curCourse.modules) {
        if (curCourse.modules.practice) {
            countPractice = curCourse.modules.practice.length
        }
        if (curCourse.modules.lectures) {
            countLectures = curCourse.modules.lectures.length
        }
        listModules = curCourse.modules.map((item, index) => {
            return (
                <ListGroup.Item 
                    as="li"
                    className="d-flex justify-content-between align-items-start"
                    key={item.title}
                >
                    <>
                        <div style={{fontSize: '14px'}} className="ms-2 me-auto">
                            <div className="fw-bold">{index+1}. {item.title}</div>
                            {item.description}
                        </div> 
                        <Badge style={{color: 'black'}} bg="primary" pill>
                           <BookOutlined style={{verticalAlign: 'bottom'}}/> 0/{countPractice} <BookOutlined/> 0/{countLectures}
                        </Badge>        
                    </>            
                </ListGroup.Item>
            )
        })
    }

    return (
        <>
            <Row>
                <Col>
                    <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Информация о курсе:</Divider>
                    {curCourse.info}
                </Col>
            </Row>
            <Row>
                <Col xs={7}>
                    <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Модули курса:</Divider>
                    <ListGroup as="ol">
                    {listModules}
                    </ListGroup>
                </Col>
                <Col>
                    <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Студенты:</Divider>
                    {listStudents}
                </Col>
            </Row>
            <Button onClick={() => handleDeleteCourse(userStore.CurCourse)} variant="outline-danger">Покинуть курс</Button>{' '}
        </>
    )
}

export default CourseInfo;