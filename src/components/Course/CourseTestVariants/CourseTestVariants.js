import React, { useContext, useState } from "react";
import 'antd/dist/antd.css';
import { Divider, message } from "antd";
import { Context } from "../../..";
import {Row, Col, Button} from "react-bootstrap"
import history from "../../../services/history";
import { COURSE_TESTS_TEST_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";
import TestEdit from "../ModalForms/CourseTestEdit";

const CourseTestVariants = () => {
    const {userStore} = useContext(Context)
    const curTest = userStore.CurTest;
    const user = userStore.User;

    const [isEsitTestFormVisible, setIsEditTestFormVisible] = useState(false)
    const [activeVariant, setActiveVariant] = useState(null)

    let listVariants = []

    const handleStartTest = () => {
        if (activeVariant === null) {
            message.error('Выберите вариант!');
        } 
        else {
            history.push(COURSE_TESTS_TEST_ROUTE);
        }
    }

    const onEditTest = () => {
        if (activeVariant === null) {
            message.error('Выберите вариант!');
        } 
        else {
            setIsEditTestFormVisible(true)
        }
    }

    const handleVariant = (variant) => {
        userStore.setCurVariant(variant);
        setActiveVariant(variant.id)
    }

    if (curTest.variants) {
        listVariants = curTest.variants.map((variant) => {
        return (
            <Button 
                key={variant.id} 
                style={{lineHeight: "0.5", marginRight: "10px"}} 
                variant="outline-secondary"
                onClick={() => handleVariant(variant)}
            >                            
                {variant.name}
            </Button>
        )
        })
    }

    if (curTest.variants) {
        return (
            <>
                <Row>
                    <Col xs={10}>
                        <Divider 
                            style={{color: 'rgb(76 86 96)', fontSize: '24px'}}
                            orientation="left"
                        >
                            {curTest.name} Варианты:
                            { isAdmin(user)
                                ? <Button style={{marginLeft: "150px"}} variant="outline-success">Добавить новый вариант</Button>
                                : null
                            }
                        </Divider>
                        {listVariants}
                    </Col>
                </Row>
                <Button 
                    style={{lineHeight: "0.8", margin: "30px 30px"}} 
                    variant="outline-success"
                    onClick={handleStartTest}
                >
                    Начать попытку
                </Button>
                { isAdmin(user)
                    ? <Button onClick={onEditTest} style={{lineHeight: "0.8", marginLeft: "30px"}} variant="outline-secondary">Редактировать тест</Button>
                    : null
                }
                <TestEdit isVisible={isEsitTestFormVisible} setIsVisible={setIsEditTestFormVisible}></TestEdit>
            </>
        )
    } 
    else {
        return (
            <Divider orientation="center">Выберите курс</Divider>
        )
    }
}

export default CourseTestVariants;