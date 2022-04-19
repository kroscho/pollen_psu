import React, { useContext, useState } from "react";
import 'antd/dist/antd.css';
import { Divider } from "antd";
import { Context } from "../../..";
import {Row, Col, ListGroup, Button} from "react-bootstrap"
import history from "../../../services/history";
import { COURSE_LECTURE_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";
import { FormOutlined } from '@ant-design/icons';
import CreateModule from "../ModalForms/CreateModule";
import CreateLectureForm from "../ModalForms/CreateLectureForm";

const CourseLections = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;
    const user = userStore.User;

    const [isCreateLectureFormVisible, setIsCreateLectureFormVisible] = useState(false)
    const [isCreateModuleFormVisible, setIsCreateModuleFormVisible] = useState(false)

    let listLectures = []
    let listModules = []

    const handleLecture = (module, lecture) => {
        userStore.setCurModule(module);
        userStore.setCurLecture(lecture);
        history.push(COURSE_LECTURE_ROUTE);
    }

    const handleCreateLecture = (module) => {
        console.log(module)
        userStore.setCurModule(module);
        setIsCreateLectureFormVisible(true)
    }

    const handleCreateModule = () => {
        setIsCreateModuleFormVisible(true)
    }

    if (curCourse.modules) {
        listLectures = (module) => {
            if (module.lectures.length === 0) {
                return (
                    <div>
                        Материалов нет
                    </div>
                )
            } else {
                return module.lectures.map((lecture) => {
                    return (
                        <div  
                            key={lecture.id} 
                            style={{cursor: 'pointer', verticalAlign: 'baseline'}} 
                            onClick={() => handleLecture(module, lecture)}
                        > 
                            <FormOutlined/> {lecture.title}
                        </div>
                    )
                })
            }
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
                        {listLectures(item)}
                    </div>
                    { isAdmin(user)
                        ?   <Button 
                            style={{verticalAlign: "bottom"}} 
                            variant="outline-success"
                            onClick={() => handleCreateLecture(item)}
                            >
                                Добавить лекцию
                            </Button>
                        : null
                    }
                    <CreateLectureForm isVisible={isCreateLectureFormVisible} setIsVisible={setIsCreateLectureFormVisible}></CreateLectureForm>                
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
                        Лекции
                    </Divider>
                    {listModules}
                    { isAdmin(user)
                        ?   <Button 
                            style={{verticalAlign: "bottom"}} 
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

export default CourseLections;