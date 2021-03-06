import React, { useContext, useEffect, useState } from "react";
import 'antd/dist/antd.css';
import { Context } from "../../..";
import {Button} from "react-bootstrap"
import history from "../../../services/history";
import { TESTS_TEST_ATTEMPTS_DETAILS_ROUTE, TESTS_TEST_ATTEMPT_ROUTE, TESTS_TEST_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";
import TestEdit from "../ModalForms/CourseTestEdit";
import ErrorMessage from "../../UI/ErrorMessage/ErrorMessage";
import Loader from "../../UI/Loader/Loader";
import { useFetching } from "../../hooks/useFetching";
import TestingApi from "../../../API/TestingApi";
import { Row } from "antd";

const CourseTestVariants = () => {
    const {userStore} = useContext(Context)
    const [attempts, setAttempts] = useState([])
    const curTest = userStore.CurTest;
    const user = userStore.User;

    const [isEsitTestFormVisible, setIsEditTestFormVisible] = useState(false)

    const [fetchAttempts, isAttemptsLoading, attemptsError] = useFetching(async () => {
        let response = await TestingApi.getAttempts(userStore.User.uid, userStore.CurTest.nameTest)
        setAttempts(response.data)
        userStore.setCurAttempts(response.data)
        console.log(response.data)
    })

    useEffect(() => {
        fetchAttempts()
    }, [])

    const [fetchDelete, isDeleteLoading, deleteError] = useFetching(async () => {
        let response = await TestingApi.deleteTest(userStore.CurTest);
        console.log(response.data)
        userStore.setCurTest({})
    })

    const handleStartTest = () => {
        history.push(TESTS_TEST_ATTEMPT_ROUTE);
    }

    const handleViewDetails = () => {
        history.push(TESTS_TEST_ATTEMPTS_DETAILS_ROUTE);
    }

    const onEditTest = () => {
        setIsEditTestFormVisible(true)
    }

    const onDeleteTest = () => {
        fetchDelete()
    }

    const View = () => {
        return (
            <>
                <Row>
                    <Button 
                        style={{lineHeight: "0.8", margin: "30px 30px"}} 
                        variant="outline-success"
                        onClick={handleStartTest}
                    >
                        ???????????? ??????????????
                    </Button>
                </Row>
                <Row style={{lineHeight: "0.8", margin: "0 30px 30px 30px"}} >
                    ?????????????????? ??????????????: {attempts.length}
                    { attempts.length != 0
                        ? <Button 
                            style={{lineHeight: "0.8", margin: "0px 30px"}} 
                            variant="outline-success"
                            onClick={handleViewDetails}
                        >
                            ???????????????????? ????????????????
                        </Button>
                        : null
                    }
                </Row>
                <Row>
                    { isAdmin(user)
                        ? <Button onClick={onEditTest} style={{lineHeight: "0.8", marginLeft: "30px"}} variant="outline-secondary">?????????????????????????? ????????</Button>
                        : null
                    }
                    { isAdmin(user)
                        ? <Button onClick={onDeleteTest} style={{lineHeight: "0.8", marginLeft: "15px"}} variant="outline-danger">?????????????? ????????</Button>
                        : null
                    }
                </Row>
                <TestEdit isVisible={isEsitTestFormVisible} setIsVisible={setIsEditTestFormVisible}></TestEdit>
            </>
        )
    }

    const spinner = isAttemptsLoading ? <Loader/> : null;
    const errorMessage = attemptsError ? <ErrorMessage message={attemptsError} /> : null;
    const content = !(isAttemptsLoading || attemptsError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )
}

export default CourseTestVariants;