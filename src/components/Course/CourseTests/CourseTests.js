import React, { useContext } from "react";
import 'antd/dist/antd.css';
import "./index.css";
import { Divider, Avatar } from "antd";
import { Context } from "../../..";
import {Row, Col, ListGroup, Button} from "react-bootstrap"
import history from "../../../services/history";
import { COURSE_TESTS_TEST_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";

const CourseTests = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;
    const user = userStore.User;

    let listTests = []
    let listVariants = []

    const handleTest = (variant, test) => {
        userStore.setCurVariant(variant);
        userStore.setCurTest(test);
        history.push(COURSE_TESTS_TEST_ROUTE);
    }

    if (curCourse.tests) {
        listVariants = (item) => {
            return item.variants.map((variant) => {
                return (
                    <Button 
                        key={variant.id} 
                        style={{lineHeight: "0.5", marginRight: "10px"}} 
                        variant="outline-secondary"
                        onClick={() => handleTest(variant, item)}
                    >                            
                        {variant.name}
                    </Button>
                )
            })
        }

        listTests = curCourse.tests.map((item) => {
            return (
                <ListGroup.Item 
                    as="li"
                    className="d-flex justify-content-between align-items-start"
                    style={{cursor: 'pointer'}}
                    key={item.id}
                >
                    <Avatar src={item.avatar} style={{marginRight: "20px"}}/>
                    <div className="ms-2 me-auto">
                        <div className="fw-bold">{item.name}</div>
                        <Row>
                            <Col xs={7}>
                                <Divider orientation="left">Попытки: {item.attempts}</Divider>
                            </Col>
                            <Col>
                                <Divider orientation="left">Варианты: {listVariants(item)}</Divider> 
                            </Col>
                        </Row>
                    </div>                    
                </ListGroup.Item>
            )
        })
    }

    if (curCourse.tests) {
        return (
            <Row>
                <Col xs={10}>
                    <Divider 
                        orientation="left"
                    >
                        { curCourse.tests.length !== 0
                            ? "Тесты:"
                            : "Тестов нет"
                        }
                        { isAdmin(user)
                            ? <Button style={{marginLeft: "150px"}} variant="outline-success">Создать тест</Button>
                            : null
                        }
                    </Divider>
                    {listTests}
                </Col>
            </Row>
        )
    } 
    else {
        return (
            <Divider orientation="center">Выберите курс</Divider>
        )
    }
}

export default CourseTests;