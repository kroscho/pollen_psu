import React, { useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Space, Select } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import EditTask from '../EditTask/EditTask';

const types = [
    { value: '1', label: 'Текстовый ответ' },
    { value: '2', label: 'Единственный ответ' },
    { value: '3', label: 'Множественный выбор' },
    { value: '4', label: 'Истина/ложь' },
];

const variants = [
    { value: '1', label: '1' },
    { value: '2', label: '2' },
    { value: '3', label: '3' },
    { value: '4', label: '4' },
]

const CreateTestForm = ({isVisible, setIsVisible}) => {
    
    const [typeQuestion, setTypeQuestion] = useState('0')
    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const [form] = Form.useForm();

    const onFinish = values => {
        console.log('Received values of form:', values);
    };

    const handleChangeType = (value) => {
        console.log(value)
        setTypeQuestion(value)
    };

    return (
        <>
        <Modal title="Создание теста" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
            <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                <Form.Item name="nameTest" label="Название теста" rules={[{ required: true, message: 'Не заполнено название теста' }]}>
                    <Input />
                </Form.Item>
                <Form.Item name="variant" label="Номер варианта" rules={[{ required: true, message: 'Не указан вариант' }]}>
                    <Select options={variants} style={{ width: 60 }} />
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
};

export default CreateTestForm;