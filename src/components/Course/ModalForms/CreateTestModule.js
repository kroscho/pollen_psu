import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Space, Select } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import EditTask from '../Task/EditTask';
import Loader from '../../UI/Loader/Loader';
import { useFetching } from '../../hooks/useFetching';
import { Context } from '../../..';
import TestingApi from '../../../API/TestingApi';
import ErrorMessage from '../../UI/ErrorMessage/ErrorMessage';

const types = [
    { value: '1', label: 'Текстовый ответ' },
    { value: '2', label: 'Единственный ответ' },
    { value: '3', label: 'Множественный выбор' },
    { value: '4', label: 'Истина/ложь' },
];

const CreateTestForm = ({isVisible, setIsVisible}) => {
    const {userStore} = useContext(Context)
    const [form] = Form.useForm();
    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const [fetchCreate, isCreateLoading, createError] = useFetching(async () => {
        let response = await TestingApi.createTest(userStore.CurTest);
        console.log(response.data)
    })

    const onFinish = values => {
        userStore.setCurTest(values);
        fetchCreate()
        //console.log('Received values of form:', values);
    };

    const handleChangeType = () => {
        const fields = form.getFieldsValue()
        form.setFieldsValue({ fields })
    };

    const View = () => {
        return (
            <>
            <Modal title="Создание теста" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                    <Form.Item name="nameTest" label="Название теста" rules={[{ required: true, message: 'Не заполнено название теста' }]}>
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
                                    prevValues.nameTest !== curValues.nameTest || prevValues.type !== curValues.type
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
                                            <Input />
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
    )
};

export default CreateTestForm;