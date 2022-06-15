import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, message } from 'antd';
import { Context } from '../../..';
import TestingApi from '../../../API/TestingApi';
import Loader from '../../UI/Loader/Loader';

const CreateSubjectArea = ({isVisible, setIsVisible, onUpdate}) => {
    
    const [url, setUrl] = useState("")
    const [subAreas, setSubAreas] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const [form] = Form.useForm();

    const {userStore} = useContext(Context)

    const fetchCreateSubjectArea = async (nameSubjectArea) => {
        setIsLoading(true)
        let response = await TestingApi.CreateSubjectArea(nameSubjectArea);
        if (response.data === "ok") {
            message.success('Предметная область добавлена успешно');
        }
        onUpdate()
        setIsVisible(false);
        setIsLoading(false)
    }

    const handleCancel = () => {
        setIsVisible(false);
    };

    const onFinish = values => {
        console.log('Received values of form:', values);
        fetchCreateSubjectArea(values.nameSubjectArea)
    };

    const View = () => {
        return (
            <>
            <Modal 
                title="Добавить предметную область" 
                visible={isVisible} 
                onCancel={handleCancel}
                footer={[
                    <Button key="back" onClick={handleCancel}>
                      Отмена
                    </Button>
                  ]}    
            >
                <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                    <Form.Item name="nameSubjectArea" label="Название предметной области" rules={[{ required: true, message: 'Не заполнено название предметной области' }]}>
                        <Input />
                    </Form.Item>
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

    const spinner = isLoading ? <Loader/> : null;
    const content = !(isLoading) ? <View/> : null;

    return (
        <>
            {spinner}
            {content}
        </>
    )
};

export default CreateSubjectArea;