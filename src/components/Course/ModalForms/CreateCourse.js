import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import TestingApi from '../../../API/TestingApi';
import { useFetching } from '../../hooks/useFetching';
import { Context } from '../../..';

const layout = {
    labelCol: {
        span: 8,
    },
    wrapperCol: {
        span: 16,
    },
};
const tailLayout = {
    wrapperCol: {
        offset: 8,
        span: 16,
    },
};

const CreateCourse = ({isVisible, setIsVisible, update, setUpdate}) => {
    
    const [url, setUrl] = useState("")
    const [form] = Form.useForm();
    const {userStore} = useContext(Context)

    const [fetchCreateCourse, isCreateLoading, createError] = useFetching(async () => {
        let response = await TestingApi.createCourse(userStore.CurNewCourse);
        console.log(response.data)
        if (response.data === "ok") {
            message.success('Курс создан успешно');
        }
        userStore.setCurTest({})
        if (update) {
            setUpdate(!update)
        }
        setIsVisible(false)
    })

    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const onReset = () => {
        form.resetFields();
    };
    
    const onFill = () => {
        form.setFieldsValue({
          name: 'Курс1',
          description: 'Описание Курса1',
          info: 'Информация о Курсе1',
        });
    };

    const onFinish = values => {
        console.log('Received values of form:', values);
        const item = {
            title: values.name,
            description: values.description,
            avatar: url,
            info: values.info,
            students: [],
            modules: [],
        }
        userStore.setCurNewCourse(item)
        fetchCreateCourse()
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
        <Modal title="Создание курса" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
            <Form {...layout} form={form} name="control-hooks" onFinish={onFinish}>
                <Form.Item
                    name="name"
                    label="Название курса"
                    rules={[
                        {
                        required: true,
                        message: 'Заполните поле',
                        },
                    ]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    name="description"
                    label="Описание курса"
                    rules={[
                        {
                        required: true,
                        message: 'Заполните поле',
                        },
                    ]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    name="info"
                    label="Информация о курсе"
                    rules={[
                        {
                        required: true,
                        message: 'Заполните поле',
                        },
                    ]}
                >
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
                <Form.Item {...tailLayout}>
                    <Button type="primary" htmlType="submit">
                        Создать
                    </Button>
                    <Button htmlType="button" onClick={onReset}>
                        Очистить
                    </Button>
                    <Button type="link" htmlType="button" onClick={onFill}>
                        Заполнить автоматически
                    </Button>
                </Form.Item>
            </Form>
        </Modal>
        </>
    );
};

export default CreateCourse;