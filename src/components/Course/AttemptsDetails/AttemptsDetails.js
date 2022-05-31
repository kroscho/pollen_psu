import React, { useContext, useEffect, useState } from "react";
import 'antd/dist/antd.css';
import { Context } from "../../..";
import { Button} from "react-bootstrap"
import { Col, Divider, Form, Input, Row, Select, Space } from "antd";
import { FormOutlined } from '@ant-design/icons';
import AttemptTask from "../Task/AttemptTask";

const AttemptsDetails = () => {
    const {userStore} = useContext(Context)
    const curTest = userStore.CurTest;
    console.log("CUrTest: ", curTest)
    const [viewDetails, setViewDetails] = useState(false)
    const [curAttempt, setCurAttempt] = useState({})
    const curAttempts = userStore.CurAttempts;
    const [form] = Form.useForm();
    let listAttempts = []

    const handleAttempt = (attempt) => {
        setCurAttempt(attempt)
        console.log("Cur Attempt: ", curAttempt)
        setViewDetails(true)
    }

    if (curAttempts) {
        listAttempts = curAttempts.map((attempt, ind) => {
            return (
                <div  
                    key={ind} 
                    style={{cursor: 'pointer', verticalAlign: 'baseline', marginTop: '20px'}} 
                    onClick={() => handleAttempt(attempt)}
                > 
                    <FormOutlined/> Попытка {ind+1}
                </div>
            )
        })
    }

    const styleResultTest = (percentComplete) => {
        let styleInput = {color: "black", fontSize: '18px'}
        if (percentComplete < 0.3) {
            styleInput.color = "red"
        } else if (percentComplete < 0.61) {
            styleInput.color = "red"
        } else if (percentComplete < 0.81) {
            styleInput.color = "orange"
        } else {
            styleInput.color = "green"
        }
        return styleInput
    }

    const View = () => {
        if (!viewDetails) {
            return (
                <Row>
                    <Col xs={10}>
                        {listAttempts}                           
                    </Col>
                </Row>
            )
        } else {
            return (
                <Form 
                form={form} 
                name="dynamic_form_nest_item"  
                autoComplete="off"
                initialValues={{
                    ["nameTest"]: curAttempt.nameTest,
                    ["tasks"]: curAttempt.tasks,
                    ["answers"]: curAttempt.tasks,
                }}
                >
                    <Form.Item>
                        <Button onClick={() => setViewDetails(false)}>Вернуться к списку попыток</Button>
                    </Form.Item>
                    <Form.Item name="nameTest">
                        <Divider 
                            style={{color: 'rgb(76 86 96)', fontSize: '22px'}}
                            orientation="center"
                        >
                            {curAttempt.nameTest}
                        </Divider>
                        <Divider 
                            style={styleResultTest(curAttempt.percentComplete)}
                            orientation="left"
                        >
                            Результат теста: {curAttempt.percentComplete * 100}%
                        </Divider>
                    </Form.Item>
                    <Form.List name="tasks">
                        {(fields) => (
                        <>
                            {fields.map(field => (
                            <Space key={field.key} style={{display: 'flex', justifyContent: 'center'}} align="baseline">
                                <Form.Item
                                style={{borderTop: '1px solid', paddingTop: "10px"}}
                                shouldUpdate={(prevValues, curValues) =>
                                    prevValues.nameTest !== curValues.nameTest || prevValues.type !== curValues.type
                                }
                                >
                                {() => (
                                    <>
                                        <Form.Item 
                                        name={[field.name, 'question']} 
                                        label="Вопрос" 
                                        >
                                            <Input />
                                        </Form.Item>
                                        <AttemptTask tasks={curAttempt.tasks} form={form} field={field}></AttemptTask>
                                    </>
                                )}
                                </Form.Item>
                            </Space>
                            ))}
                        </>
                        )}
                    </Form.List>
                </Form>
            )
        }
    }

    return (
        <>
            <View></View>
        </>
    )
}

export default AttemptsDetails;