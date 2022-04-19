import React, { useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Upload, Avatar } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const CreateModule = ({isVisible, setIsVisible}) => {
    
    const [url, setUrl] = useState("")

    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const [form] = Form.useForm();

    const onFinish = values => {
        //console.log('Received values of form:', values);
        const item = {
            title: values.nameModule,
            description: values.descrModule,
            avatar: url,
            practice: [],
            lectures: [],
            tests: [],
        }
        console.log(item)
    };

    const normFile = (e) => {
        if (e.fileList && e.fileList[0] && e.fileList[0].thumbUrl) {
            //console.log('Upload event:', e.fileList[0].thumbUrl);
            setUrl(e.fileList[0].thumbUrl)
        } else {
            setUrl("")
        }
      
        if (Array.isArray(e)) {
          return e;
        }
      
        return e && e.fileList;
      };

    return (
        <>
        <Modal title="Создание модуля" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
            <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                <Form.Item name="nameModule" label="Название модуля" rules={[{ required: true, message: 'Не заполнено название модуля' }]}>
                    <Input />
                </Form.Item>
                <Form.Item name="descrModule" label="Описание модуля" rules={[{ required: true, message: 'Не заполнено описание модуля' }]}>
                    <Input />
                </Form.Item>
                <Form.Item
                    name="upload"
                    label="Upload"
                    valuePropName="fileList"
                    getValueFromEvent={normFile}
                >
                    <Upload name="logo" listType="picture">
                        <Button icon={<UploadOutlined />}>Click to upload</Button>
                    </Upload>
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
};

export default CreateModule;