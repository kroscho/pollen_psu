import React, { useContext, useEffect, useState } from "react";
import 'antd/dist/antd.css';
import { Divider  } from "antd";
import { Context } from "../../..";
import {Row, Col } from "react-bootstrap"
import TestingApi from "../../../API/TestingApi";
import { useFetching } from "../../hooks/useFetching";
import Loader from "../../UI/Loader/Loader";
import ErrorMessage from "../../UI/Messages/ErrorMessage";

const TermsPage = () => {
    const {userStore} = useContext(Context)
    const curCourse = userStore.CurCourse;
    const user = userStore.User;

    const [fetchTermsByUser, isDataLoading, dataError] = useFetching(async () => {
        let response = await TestingApi.getTermsByUSer(user.userObj);
        console.log(response.data)
    })

    useEffect(() => {
        fetchTermsByUser()
    }, [])

    const View = () => {
        return (
            <>
                <Row>
                    <Col>
                        <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Термины:</Divider>
                    </Col>
                </Row>
            </>
        )
    }

    const spinner = isDataLoading ? <Loader/> : null;
    const errorMessage = dataError ? <ErrorMessage message={dataError} /> : null;
    const content = !(isDataLoading || dataError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )
}

export default TermsPage;