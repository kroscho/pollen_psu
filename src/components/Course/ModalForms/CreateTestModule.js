import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Space, Select, message } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import EditTask from '../Task/EditTask';
import { useFetching } from '../../hooks/useFetching';
import { Context } from '../../..';
import TestingApi from '../../../API/TestingApi';
import { MULTIPLE_TASK_TYPE, SINGLE_TASK_TYPE } from '../../../utils/consts';

const types = [
    { value: '1', label: 'Текстовый ответ' },
    { value: '2', label: 'Единственный ответ' },
    { value: '3', label: 'Множественный выбор' },
    { value: '4', label: 'Истина/ложь' },
];

const CreateTestForm = ({isVisible, setIsVisible, module, onUpdate}) => {
    const {userStore} = useContext(Context)
    const [answers, setAnswers] = useState([])
    const [valueQuestion, setValueQuestion] = useState("")
    //const [fieldKey, setFieldKey] = useState(0)
    const [form] = Form.useForm();
    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const [fetchCreate, isCreateLoading, createError] = useFetching(async () => {
        const item = {test: userStore.CurTest, module: userStore.CurModule}
        let response = await TestingApi.createTest(item);
        if (response.data === "ok") {
            message.success('Тест создан успешно');
        }
        let response1 = await TestingApi.getCourseInfo(userStore.CurCourse.courseObj);
        userStore.setCurCourse(response1.data)
        onUpdate()
        setIsVisible(false)
        console.log(response.data)
    })

    const [fetchAnswersAuto, isDataLoading, dataError] = useFetching(async () => {
        let response = await TestingApi.getAnswersAuto(userStore.CurModule.subjectArea, userStore.CurQuestion);
        handle(response.data)
    })

    const onFinish = values => {
        userStore.setCurTest(values);
        fetchCreate()
        console.log('Received values of form:', values);
    };

    const handleChangeType = () => {
        const fields = form.getFieldsValue()
        console.log("fields: ", fields)
        form.setFieldsValue({ fields })
    };

    const handle = (data) => {
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

    const handleGenerateAnswers = (field) => {
        console.log("fieldKey: ", field)
        userStore.setCurFieldKey(field)
        userStore.setCurQuestion(valueQuestion)
        fetchAnswersAuto()
    }
    
    return (
        <>
        <Modal title="Создание теста" visible={isVisible} onOk={handleOk} onCancel={handleCancel} width={600}>
            <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                <Form.Item name="testName" label="Название теста" rules={[{ required: true, message: 'Не заполнено название теста' }]}>
                    <Input/>
                </Form.Item>
                <Form.List name="tasks">
                    {(fields, { add, remove }) => (
                    <>
                        {fields.map(field => (
                        <Space key={field.key} style={{display: 'flex', justifyContent: 'center'}}>
                            { !isDataLoading
                                ?   <Form.Item
                                        style={{borderTop: '1px solid', width: "100%"}}
                                        shouldUpdate={(prevValues, curValues) =>
                                            prevValues.type !== curValues.type
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
                                                    <Select options={types} style={{ width: 200 }} onChange={handleChangeType} />
                                                </Form.Item>
                                                <Form.Item 
                                                name={[field.name, 'question']} 
                                                label="Текст вопроса" 
                                                rules={[{ required: true, message: 'Не заполнен текст вопроса' }]}
                                                >
                                                    <Input value={valueQuestion} onChange={(e) => setValueQuestion(e.target.value)}/>
                                                </Form.Item>
                                                <Form.Item>
                                                    <Button onClick={() => handleGenerateAnswers(field.key)} type="dashed">Сгенерировать ответы</Button>
                                                </Form.Item>
                                            <EditTask form={form} field={field}></EditTask>
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
                    Добавить
                    </Button>
                </Form.Item>
            </Form>
        </Modal>
        </>
    );

    /*const View = () => {
        return (
            <>
            <Modal title="Создание теста" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                    <Form.Item name="testName" label="Название теста" rules={[{ required: true, message: 'Не заполнено название теста' }]}>
                        <Input/>
                    </Form.Item>
                    <Form.List name="tasks">
                        {(fields, { add, remove }) => (
                        <>
                            {fields.map(field => (
                            <Space key={field.key} style={{display: 'flex', justifyContent: 'center'}} align="baseline">
                                <Form.Item
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
                                            <Select options={types} style={{ width: 200 }} onChange={handleChangeType} />
                                        </Form.Item>
                                        <Form.Item 
                                        name={[field.name, 'question']} 
                                        label="Текст вопроса" 
                                        rules={[{ required: true, message: 'Не заполнен текст вопроса' }]}
                                        >
                                            <Input onChange={handleChangeQuestion}/>
                                        </Form.Item>
                                       <EditTask form={form} field={field}></EditTask>
                                    </>
                                )}
                                </Form.Item>
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
                        Добавить
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
            </>
        );
    }

    const spinner = isCreateLoading ? <Loader/> : null;
    const errorMessage = createError ? <ErrorMessage message="Тест с таким названием уже существует" /> : null;
    const content = !(isCreateLoading || createError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )*/
};

export default CreateTestForm;