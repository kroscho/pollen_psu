import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, Upload, Avatar, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { Context } from '../../..';
import { useFetching } from '../../hooks/useFetching';
import TestingApi from '../../../API/TestingApi';
import Loader from '../../UI/Loader/Loader';
import ErrorMessage from '../../UI/Messages/ErrorMessage';

const CreateModule = ({isVisible, setIsVisible, setCurCourse}) => {
    
    const [url, setUrl] = useState("")
    const [form] = Form.useForm();

    const {userStore} = useContext(Context)

    const [fetchCreateModule, isCreateLoading, createError] = useFetching(async () => {
        const item = {module: userStore.CurModule, courseObj: userStore.CurCourse.courseObj}
        let response = await TestingApi.createModule(item);
        if (response.data === "ok") {
            message.success('Модуль создан успешно');
        }
        let response1 = await TestingApi.getCourseInfo(userStore.CurCourse.courseObj);
        userStore.setCurCourse(response1.data)
        setCurCourse(userStore.CurCourse)
        console.log(response.data)
        userStore.setCurModule({})
        setIsVisible(false);
    })

    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const onFinish = values => {
        //console.log('Received values of form:', values);
        const item = {
            nameModule: values.nameModule,
            avatar: url,
            practice: [],
            lectures: [],
            tests: [],
        }
        userStore.setCurModule(item)
        fetchCreateModule()
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

    const View = () => {
        return (
            <>
            <Modal title="Создание модуля" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                    <Form.Item name="nameModule" label="Название модуля" rules={[{ required: true, message: 'Не заполнено название модуля' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="upload"
                        label="Upload"
                        valuePropName="fileList"
                        getValueFromEvent={normFile}
                    >
                        <Upload name="logo" listType="picture">
                            <Button icon={<UploadOutlined />}>Загрузить фото</Button>
                        </Upload>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                        Создать
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
            </>
        );
    }

    const spinner = isCreateLoading ? <Loader/> : null;
    const errorMessage = createError ? <ErrorMessage message={createError} /> : null;
    const content = !(isCreateLoading || createError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )
};

export default CreateModule;