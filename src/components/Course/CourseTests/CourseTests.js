import React, { useContext, useEffect, useState } from "react";
import 'antd/dist/antd.css';
import { Divider } from "antd";
import { Context } from "../../..";
import {Row, Col, Button} from "react-bootstrap"
import history from "../../../services/history";
import { TESTS_TEST_ATTEMPT_ROUTE, TESTS_TEST_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";
import { FormOutlined } from '@ant-design/icons';
import CreateTestForm from "../ModalForms/CreateTestModule";
import { useFetching } from "../../hooks/useFetching";
import TestingApi from "../../../API/TestingApi";
import Loader from "../../UI/Loader/Loader";

const CourseTests = () => {
    const {userStore, services} = useContext(Context)
    const user = userStore.User;
    //const tests = services.Tests;
    const [isCreateTestFormVisible, setIsCreateTestFormVisible] = useState(false)
    const [tests, setTests] = useState([])
    let listTests = []

    const [fetchTests, isDataLoading, itemsError] = useFetching(async () => {
        let response = await TestingApi.getTests()
        setTests(response.data)
        console.log(response.data)
    })

    useEffect(() => {
        fetchTests()
    }, [])

    const handleTest = (test) => {
        userStore.setCurTest(test);
        history.push(TESTS_TEST_ROUTE);
    }

    const handleCreateTest = () => {
        setIsCreateTestFormVisible(true)
    }

    if (tests) {
        listTests = tests.map((test, ind) => {
            return (
                <div  
                    key={ind} 
                    style={{cursor: 'pointer', verticalAlign: 'baseline', marginTop: '20px'}} 
                    onClick={() => handleTest(test)}
                > 
                    <FormOutlined/> {test.nameTest}
                </div>
            )
        })
    }

    const View = () => {
        return (
            <Row>
                <Col xs={10}>
                    <Divider 
                        style={{color: 'rgb(76 86 96)', fontSize: '24px'}}
                        orientation="left"
                    >
                        { (listTests.length !== 0)
                            ? "Тесты:"
                            : "Тестов нет"
                        }
                    </Divider>
                    {listTests}
                    { isAdmin(user)
                        ?   <Button 
                            style={{verticalAlign: "bottom", marginTop: '20px'}} 
                            variant="outline-success"
                            onClick={handleCreateTest}
                            >
                                Создать тест
                            </Button>
                        : null
                    }
                    <CreateTestForm isVisible={isCreateTestFormVisible} setIsVisible={setIsCreateTestFormVisible}></CreateTestForm>                             
                </Col>
            </Row>
        )
    }

    const spinner = isDataLoading ? <Loader/> : null;
    const content = !(isDataLoading || itemsError) ? <View/> : null;

    return (
        <>
            {spinner}
            {content}
        </>
    )
}

export default CourseTests;