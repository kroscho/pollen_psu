import React, { useContext, useState } from "react";
import 'antd/dist/antd.css';
import { Context } from "../../..";
import {Button} from "react-bootstrap"
import history from "../../../services/history";
import { TESTS_TEST_ATTEMPT_ROUTE, TESTS_TEST_ROUTE } from "../../../utils/consts";
import { isAdmin } from "../../utils/testing";
import TestEdit from "../ModalForms/CourseTestEdit";
import ErrorMessage from "../../UI/ErrorMessage/ErrorMessage";
import Loader from "../../UI/Loader/Loader";
import { useFetching } from "../../hooks/useFetching";
import TestingApi from "../../../API/TestingApi";
import { Row } from "antd";

const CourseTestVariants = () => {
    const {userStore} = useContext(Context)
    const curTest = userStore.CurTest;
    const user = userStore.User;

    const [isEsitTestFormVisible, setIsEditTestFormVisible] = useState(false)

    const [fetchDelete, isDeleteLoading, deleteError] = useFetching(async () => {
        let response = await TestingApi.deleteTest(userStore.CurTest);
        console.log(response.data)
        userStore.setCurTest({})
    })

    const handleStartTest = () => {
        history.push(TESTS_TEST_ATTEMPT_ROUTE);
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
                        Начать попытку
                    </Button>
                </Row>
                <Row>
                    { isAdmin(user)
                        ? <Button onClick={onEditTest} style={{lineHeight: "0.8", marginLeft: "30px"}} variant="outline-secondary">Редактировать тест</Button>
                        : null
                    }
                    { isAdmin(user)
                        ? <Button onClick={onDeleteTest} style={{lineHeight: "0.8", marginLeft: "15px"}} variant="outline-danger">Удалить тест</Button>
                        : null
                    }
                </Row>
                <TestEdit isVisible={isEsitTestFormVisible} setIsVisible={setIsEditTestFormVisible}></TestEdit>
            </>
        )
    }

    const spinner = isDeleteLoading ? <Loader/> : null;
    const errorMessage = deleteError ? <ErrorMessage message={deleteError} /> : null;
    const content = !(isDeleteLoading || deleteError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )
}

export default CourseTestVariants;