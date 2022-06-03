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

const types = [
    { value: '1', label: 'Текстовый ответ' },
    { value: '2', label: 'Единственный ответ' },
    { value: '3', label: 'Множественный выбор' },
    { value: '4', label: 'Логический' },
];

const TestEdit = ({isVisible, setIsVisible}) => {
    const {userStore} = useContext(Context)
    const [curTest, setCurTest] = useState(userStore.CurTest)
    const [form] = Form.useForm();

    const [fetchTest, isDataLoading, testError] = useFetching(async () => {
        let response = await TestingApi.getTestWithAnswers(curTest.testName);
        setCurTest(response.data)
        console.log(response.data)
    })

    const [fetchUpdate, isUpdateLoading, updateError] = useFetching(async () => {
        let response = await TestingApi.updateTest(userStore.CurTest);
        console.log(response.data)
    })

    useEffect(() => {
        fetchTest()
    }, [])

    const handleCancel = () => {
        form.setFieldsValue({ testName: curTest.testName, tasks: curTest.tasks, answers: curTest.tasks})
        setIsVisible(false);
    };

    const onChangeType = () => {
        const fields = form.getFieldsValue()
        form.setFieldsValue({ fields })
    }


    const onFinish = values => {
        const isEqual = deepEqual(values, curTest)
        if (!isEqual) {
            values["prevNameTest"] = curTest.testName;
            userStore.setCurTest(values);
            fetchUpdate()
        }
        console.log('Received values of form:', values);
    };

    const View = () => {
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
                                            <Select options={types} style={{ width: 200 }} onChange={onChangeType} />
                                        </Form.Item>
                                        <Form.Item 
                                        name={[field.name, 'question']} 
                                        label="Текст вопроса" 
                                        rules={[{ required: true, message: 'Не заполнен текст вопроса' }]}
                                        >
                                            <Input />
                                        </Form.Item>
                                    <EditTask tasks={curTest.tasks} form={form} field={field}></EditTask>
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
                        Сохранить изменения
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
            </>
        )
    }

    const spinner = isDataLoading ? <Loader/> : null;
    const content = !(isDataLoading || isUpdateLoading || testError || updateError) ? <View/> : null;

    return (
        <>
            {spinner}
            {content}
        </>
    )
}

export default TestEdit;