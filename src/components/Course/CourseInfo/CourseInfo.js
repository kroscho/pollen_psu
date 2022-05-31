import React, { useContext, useEffect, useState } from "react";
import 'antd/dist/antd.css';
import { Divider, Avatar, message } from "antd";
import { Context } from "../../..";
import {Row, Col, ListGroup, Button, Badge} from "react-bootstrap"
import { BookOutlined } from '@ant-design/icons';
import TestingApi from "../../../API/TestingApi";
import { useFetching } from "../../hooks/useFetching";
import Loader from "../../UI/Loader/Loader";
import ErrorMessage from "../../UI/Messages/ErrorMessage";
import { isAdmin } from "../../utils/testing";
import { TESTING_ALL_COURSES_ROUTE } from "../../../utils/consts";
import history from "../../../services/history";
import UsersList from "../Users/UsersList";

const CourseInfo = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;
    const [students, setStudents] = useState([])
    const [modules, setModules] = useState([])
    const [update, setUpdate] = useState(true)
    const user = userStore.User;

    let listStudents = []
    let listModules = []
    let countPractice = 0
    let countLectures = 0

    const [fetchCourseInfo, isDataLoading, dataError] = useFetching(async () => {
        let response = await TestingApi.getCourseInfo(userStore.CurCourse.courseObj);
        userStore.setCurCourse(response.data)
        setStudents(response.data.students)
        setModules(response.data.modules)
        console.log(response.data)
    })

    const [fetchSubscribeCourse, isSubscribeLoading, subscribeError] = useFetching(async () => {
        const item = {uid: userStore.User.uid, courseObj: userStore.CurCourse.courseObj}
        let response = await TestingApi.subscribeCourse(item);
        if (response.data === "ok") {
            message.success('Вы подписались на курс успешно');
        }
        let response2 = await TestingApi.getUserCourses(userStore.User.uid);
        userStore.setMyCourses(response2.data)
        setUpdate(!update)
    })

    const [fetchUnsubscribeCourse, isUnsubscribeLoading, unsubscribeError] = useFetching(async () => {
        const item = {uid: userStore.User.uid, courseObj: userStore.CurCourse.courseObj}
        let response = await TestingApi.unsubscribeCourse(item);
        if (response.data === "ok") {
            message.success('Вы отписались от курса успешно');
        }
        let response2 = await TestingApi.getUserCourses(userStore.User.uid);
        userStore.setMyCourses(response2.data)
        setUpdate(!update)
    })

    const [fetchDeleteCourse, isDeleteLoading, deleteError] = useFetching(async () => {
        let response = await TestingApi.deleteCourse(userStore.CurCourse);
        if (response.data === "ok") {
            message.success('Курс удалён успешно');
        }
        history.push(TESTING_ALL_COURSES_ROUTE);
    })

    useEffect(() => {
        fetchCourseInfo()
    }, [update])

    const handleSubscribeCourse = () => {
        fetchSubscribeCourse()
    }

    const handleUnsubscribeCourse = () => {
        fetchUnsubscribeCourse()
    }

    const handleDeleteCourse = () => {
        fetchDeleteCourse()
    }

    const isSubscribe = () => {
        const courses = userStore.MyCourses.filter(elem => elem.courseName === userStore.CurCourse.courseName)
        return courses.length > 0 ? true : false
    }

    if (students) {
        listStudents = students.map((item) => {
            return (
                <ListGroup.Item 
                    as="li"
                    className="d-flex justify-content-between align-items-start"
                    key={item.uid}
                >
                    <Avatar src="https://joeschmoe.io/api/v1/random" style={{marginRight: "20px"}}/>
                    <div className="ms-2 me-auto">
                        {item.firstName} {item.lastName}
                    </div>                    
                </ListGroup.Item>
            )
        })
    }

    if (modules) {
        if (modules.practice) {
            countPractice = curCourse.modules.practice.length
        }
        if (modules.lectures) {
            countLectures = curCourse.modules.lectures.length
        }
        listModules = modules.map((item, index) => {
            return (
                <ListGroup.Item 
                    as="li"
                    className="d-flex justify-content-between align-items-start"
                    key={index}
                >
                    <>
                        <div style={{fontSize: '14px'}} className="ms-2 me-auto">
                            <div className="fw-bold">{index+1}. {item.nameModule}</div>
                        </div> 
                        <Badge style={{color: 'black'}} bg="primary" pill>
                           <BookOutlined style={{verticalAlign: 'bottom'}}/> 0/{countPractice} <BookOutlined/> 0/{countLectures}
                        </Badge>        
                    </>            
                </ListGroup.Item>
            )
        })
    }

    const View = () => {
        return (
            <>
                <Row>
                    <Col>
                        <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Информация о курсе:</Divider>
                        {curCourse.courseInfo}
                    </Col>
                </Row>
                <Row>
                    { isAdmin(user)
                        ? <Col><Button onClick={handleDeleteCourse} style={{margin: "15px 0 0 20px"}} variant="outline-danger">Удалить курс</Button></Col>
                        : null
                    }
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
                        <UsersList users={students}/>
                    </Col>
                </Row>
                {isSubscribe()
                    ? <Button onClick={() => handleUnsubscribeCourse(userStore.CurCourse)} variant="outline-danger">Покинуть курс</Button>
                    : <Button onClick={() => handleSubscribeCourse(userStore.CurCourse)} variant="outline-success">Подписаться на курс</Button>
                }
            </>
        )
    }

    const spinner = isDataLoading || isSubscribeLoading || isUnsubscribeLoading ? <Loader/> : null;
    const errorMessage = dataError || subscribeError || unsubscribeError ? <ErrorMessage message={dataError} /> : null;
    const content = !(isDataLoading || isSubscribeLoading || isUnsubscribeLoading || dataError || subscribeError || unsubscribeError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )
}

export default CourseInfo;