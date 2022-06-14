import React, { useContext, useEffect, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Space, Select } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import { Context } from '../../..';
import EditTask from '../Task/EditTask';
import TestingApi from '../../../API/TestingApi';
import { useFetching } from '../../hooks/useFetching';
import Loader from '../../UI/Loader/Loader';
import { deepEqual } from '../../utils/testing';
import TextArea from 'antd/lib/input/TextArea';
import { MULTIPLE_TASK_TYPE } from '../../../utils/consts';

const types = [
    { value: '1', label: 'Текстовый ответ' },
    { value: '2', label: 'Единственный ответ' },
    { value: '3', label: 'Множественный выбор' },
    { value: '4', label: 'Логический' },
];

const TestEdit = ({isVisible, setIsVisible}) => {
    const {userStore} = useContext(Context)
    const [curTest, setCurTest] = useState(userStore.CurTest)
    const [valueQuestion, setValueQuestion] = useState("")
    const [answers, setAnswers] = useState([])
    const [terms, setTerms] = useState([])
    const [form] = Form.useForm();

    const [fetchTest, isDataLoading, testError] = useFetching(async () => {
        let response = await TestingApi.getTestWithAnswers(curTest.testName);
        setCurTest(response.data)
        let response2 = await TestingApi.getTermsBySubjArea(userStore.CurModule.subjectArea);
        setTerms(response2.data)
        console.log(response.data)
    })

    const [fetchUpdate, isUpdateLoading, updateError] = useFetching(async () => {
        let response = await TestingApi.updateTest(userStore.CurTest);
        console.log(response.data)
    })

    const [fetchAnswersAuto, isAnswersLoading, answersError] = useFetching(async () => {
        let response = await TestingApi.getAnswersAuto(userStore.CurModule.subjectArea, userStore.CurQuestion);
        updateFormAnswers(response.data)
    })

    useEffect(() => {
        fetchTest()
    }, [])

    const updateFormAnswers = (data) => {
        const fieldKey = userStore.СurFieldKey
        console.log("fieldKey: ", fieldKey)
        let answersCopy = answers.slice()
        answersCopy[fieldKey] = data
        let fields = form.getFieldsValue()
        if (answersCopy) {
            fields.tasks[fieldKey].answers = []
            for (let item of answersCopy[fieldKey]) {
                console.log("item: ", item)
                fields.tasks[fieldKey].answers.push(item)
            }
            fields.tasks[fieldKey].type = MULTIPLE_TASK_TYPE
            form.setFieldsValue({ fields })
            console.log(fields)
            setAnswers(answersCopy)
        }
    }

    const handleCancel = () => {
        form.setFieldsValue({ testName: curTest.testName, tasks: curTest.tasks, answers: curTest.tasks})
        setIsVisible(false);
    };

    const handleGenerateAnswers = (field) => {
        console.log("fieldKey: ", field)
        userStore.setCurFieldKey(field)
        userStore.setCurQuestion(valueQuestion)
        fetchAnswersAuto()
    }

    const onChangeType = () => {
        const fields = form.getFieldsValue()
        form.setFieldsValue({ fields })
    }

    const listTerms = terms.map((item) => {
        return {value: item.term, label: item.termStr}
    })

    const onFinish = values => {
        const isEqual = deepEqual(values, curTest)
        if (!isEqual) {
            values["prevNameTest"] = curTest.testName;
            userStore.setCurTest(values);
            fetchUpdate()
        }
        console.log('Received values of form:', values);
    };

    if (isDataLoading || isUpdateLoading) {
        return <Loader/>
    } else {
        return (
            <>
            <Modal 
            title="Редактирование теста" 
            visible={isVisible}
            onCancel={handleCancel}
            footer={[
                <Button key="back" onClick={handleCancel}>
                  Отмена
                </Button>
              ]}
            >
                <Form 
                form={form} 
                name="dynamic_form_nest_item" 
                onFinish={onFinish} 
                autoComplete="off"
                initialValues={{
                    ["testName"]: curTest.testName,
                    ["tasks"]: curTest.tasks,
                    ["answers"]: curTest.tasks,
                }}
                >
                    <Form.Item name="testName" label="Название теста" rules={[{ required: true, message: 'Не заполнено название теста' }]}>
                        <Input />
                    </Form.Item>
                    <Form.List name="tasks">
                        {(fields, { add, remove }) => (
                        <>
                            {fields.map(field => (
                            <Space key={field.key} style={{display: 'flex', justifyContent: 'center'}} align="baseline">
                                { !isAnswersLoading
                                    ?   <Form.Item
                                        style={{borderTop: '1px solid'}}
                                        shouldUpdate={(prevValues, curValues) =>
                                            prevValues.testName !== curValues.testName || prevValues.type !== curValues.type
                                        }
                                        >
                                        {() => (
                                            <>
                                                <Form.Item
                                                {...field}
                                                label="Тип вопроса"
                                                name={[field.name, 'type']}
                                                rules={[{ required: true, message: 'Missing type' }]}
                                                style={{ margin: '10px auto'}}
                                                >
                                                    <Select options={types} style={{ width: 200 }} onChange={onChangeType} />
                                                </Form.Item>
                                                <Form.Item 
                                                name={[field.name, 'question']} 
                                                label="Текст вопроса" 
                                                rules={[{ required: true, message: 'Не заполнен текст вопроса' }]}
                                                >
                                                    <TextArea rows={4} value={valueQuestion} onChange={(e) => setValueQuestion(e.target.value)}></TextArea>
                                                </Form.Item>
                                                <Form.Item
                                                label="Концепт: "
                                                name={[field.name, 'term']}
                                                rules={[{ required: true, message: 'Missing type' }]}
                                                style={{ margin: '10px auto', pointerEvents: true}}
                                                >
                                                    <Select
                                                    showSearch
                                                    style={{
                                                    width: 300,
                                                    }}
                                                    placeholder="Искать концепт"
                                                    optionFilterProp="children"
                                                    filterOption={(input, option) => option.label.toLowerCase().includes(input.toLowerCase())}
                                                    filterSort={(optionA, optionB) =>
                                                        optionA.children.toLowerCase().localeCompare(optionB.children.toLowerCase())
                                                    }
                                                    options={listTerms}
                                                    >
                                                    </Select>
                                                </Form.Item>
                                                <Form.Item>
                                                    <Button onClick={() => handleGenerateAnswers(field.key)} type="dashed">Сгенерировать ответы</Button>
                                                </Form.Item>
                                            <EditTask tasks={curTest.tasks} form={form} field={field}></EditTask>
                                            </>
                                        )}
                                        </Form.Item>
                                    : null
                                }
                                <MinusCircleOutlined onClick={() => remove(field.name)} />
                            </Space>
                            ))}

                            <Form.Item>
                            <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                                Добавить задание
                            </Button>
                            </Form.Item>
                        </>
                        )}
                    </Form.List>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                        Сохранить изменения
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
            </>
        )
    }
}

export default TestEdit;