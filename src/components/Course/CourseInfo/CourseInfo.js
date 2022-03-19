import React, { useContext } from "react";
import 'antd/dist/antd.css';
import "./index.css";
import { Divider, Avatar } from "antd";
import { Context } from "../../..";
import {Row, Col, ListGroup, Button} from "react-bootstrap"

const CourseInfo = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;

    let listStudents = []

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

    return (
        <>
            <Row>
                <Col xs={7}>
                    <Divider orientation="left">Информация о курсе:</Divider>
                    {curCourse.info}
                </Col>
                <Col>
                    <Divider orientation="left">Студенты:</Divider>
                    {listStudents}
                </Col>
            </Row>
            <Button variant="outline-danger">Покинуть курс</Button>{' '}
        </>
    )
}

export default CourseInfo;