import React, { useContext, useEffect, useState } from "react";
import 'antd/dist/antd.css';
import { Collapse, Divider, List  } from "antd";
import { Context } from "../../..";
import {Row, Col } from "react-bootstrap"
import TestingApi from "../../../API/TestingApi";
import { useFetching } from "../../hooks/useFetching";
import Loader from "../../UI/Loader/Loader";
import ErrorMessage from "../../UI/Messages/ErrorMessage";
const { Panel } = Collapse;

const TermsPage = () => {
    const {userStore} = useContext(Context)
    const [subAreas, setSubAreas] = useState([])
    const [terms, setTerms] = useState({})
    const curCourse = userStore.CurCourse;
    const user = userStore.User;

    const [fetchTermsByUser, isDataLoading, dataError] = useFetching(async () => {
        let response = await TestingApi.getTermsByUser(user.userObj);
        setTerms(response.data)
        console.log(response.data)
        let response1 = await TestingApi.getSubjectAreas();
        setSubAreas(response1.data)
        console.log(response1.data)
    })

    useEffect(() => {
        fetchTermsByUser()
    }, [])

    const listSubjAreas = subAreas.map((subjArea, ind) => {
        const knownTerms = terms.knownTerms.filter(item => item.subjectArea === subjArea.subjectAreaObj)
        const unknownTerms = terms.unknownTerms.filter(item => item.subjectArea === subjArea.subjectAreaObj)

        return (
            <Panel header={subjArea.subjectArea} key={ind}>
                <Divider orientation="left">Плохо изучены:</Divider>
                <List
                    size="small"
                    bordered
                    style={{borderColor: 'red'}}
                    dataSource={unknownTerms}
                    renderItem={(term) => <List.Item>{term.term}</List.Item>}
                />
                <Divider orientation="left">Хорошо изучены:</Divider>
                <List
                    size="small"
                    header={<div>Хорошо знает</div>}
                    bordered
                    style={{borderColor: 'green'}}
                    dataSource={knownTerms}
                    renderItem={(term) => <List.Item>{term.term}</List.Item>}
                />
            </Panel>
        )
    })

    const View = () => {
        return (
            <>
                <Row>
                    <Col>
                        <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Термины:</Divider>
                        <Collapse accordion>
                            {listSubjAreas}
                        </Collapse>
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