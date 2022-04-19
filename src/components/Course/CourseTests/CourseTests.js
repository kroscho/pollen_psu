import React, { useContext, useState } from "react";
import 'antd/dist/antd.css';
import { Divider } from "antd";
import { Context } from "../../..";
import {Row, Col, ListGroup, Button} from "react-bootstrap"
import history from "../../../services/history";
import { COURSE_TESTS_TEST_VARIANTS_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";
import { FormOutlined } from '@ant-design/icons';
import CreateTestForm from "../ModalForms/CreateTestModule";
import CreateModule from "../ModalForms/CreateModule";

const CourseTests = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;
    const user = userStore.User;

    const [isCreateTestFormVisible, setIsCreateTestFormVisible] = useState(false)
    const [isCreateModuleFormVisible, setIsCreateModuleFormVisible] = useState(false)

    let listTests = []
    let listModules = []

    const handleTest = (module, test) => {
        userStore.setCurModule(module);
        userStore.setCurTest(test);
        history.push(COURSE_TESTS_TEST_VARIANTS_ROUTE);
    }

    const handleCreateTest = () => {
        setIsCreateTestFormVisible(true)
    }

    const handleCreateModule = () => {
        setIsCreateModuleFormVisible(true)
    }

    if (curCourse.modules) {
        listTests = (module) => {
            return module.tests.map((test) => {
                return (
                    <div  
                        key={test.id} 
                        style={{cursor: 'pointer', verticalAlign: 'baseline'}} 
                        onClick={() => handleTest(module, test)}
                    > 
                        <FormOutlined/> {test.name}
                    </div>
                )
            })
        }

        listModules = curCourse.modules.map((item) => {
            return (
                <ListGroup.Item 
                    as="li"
                    className="d-flex justify-content-between align-items-start"
                    style={{color: '#6287ab'}}
                    key={item.id}
                >
                    <div className="ms-2 me-auto">
                        <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">{item.title}</Divider>
                        {listTests(item)}
                    </div>
                    { isAdmin(user)
                        ?   <Button 
                            style={{verticalAlign: "bottom"}} 
                            variant="outline-success"
                            onClick={handleCreateTest}
                            >
                                Создать тест
                            </Button>
                        : null
                    }
                    <CreateTestForm isVisible={isCreateTestFormVisible} setIsVisible={setIsCreateTestFormVisible}></CreateTestForm>                
                </ListGroup.Item>
            )
        })
    }

    if (curCourse.modules) {
        return (
            <Row>
                <Col xs={10}>
                    <Divider 
                        style={{color: 'rgb(76 86 96)', fontSize: '24px'}}
                        orientation="left"
                    >
                        { (curCourse.modules[0] && curCourse.modules[0].tests && curCourse.modules[0].tests.length !== 0)
                            ? "Тесты:"
                            : "Тестов нет"
                        }
                    </Divider>
                    {listModules}
                    { isAdmin(user)
                        ?   <Button 
                            style={{verticalAlign: "bottom", marginTop: "20px"}} 
                            variant="outline-success"
                            onClick={handleCreateModule}
                            >
                                Добавить модуль
                            </Button>
                        : null
                    }             
                </Col>
                <CreateModule isVisible={isCreateModuleFormVisible} setIsVisible={setIsCreateModuleFormVisible}></CreateModule>
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