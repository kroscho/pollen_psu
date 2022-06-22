import React, { useEffect, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, message, Select } from 'antd';
import { useFetching } from '../../hooks/useFetching';
import TestingApi from '../../../API/TestingApi';
import Loader from '../../UI/Loader/Loader';
import { CUR_COURSE_STORAGE } from '../../../utils/consts';
import { getLocalStorage, setLocalStorage } from '../../utils/testing';
const { Option } = Select;

const CreateModule = ({isVisible, setIsVisible, onUpdate}) => {
    
    const [url, setUrl] = useState("")
    const [subAreas, setSubAreas] = useState([])
    const [isLoading, setIsLoading] = useState(false)

    const [form] = Form.useForm();

    const curCourse = getLocalStorage(CUR_COURSE_STORAGE)

    const [fetchSubjectAreas, isDataLoading, dataError] = useFetching(async () => {
        let response = await TestingApi.getSubjectAreas();
        setSubAreas(response.data)
    })

    const fetchCreateModule = async (module) => {
        setIsLoading(true)
        try {
            const item = {module: module, courseObj: curCourse.courseObj}
            let response = await TestingApi.createModule(item);
            if (response.data === "ok") {
                message.success('Модуль создан успешно');
            }
            let response1 = await TestingApi.getCourseInfo(curCourse.courseObj);
            setLocalStorage(CUR_COURSE_STORAGE,response1.data)
            setIsVisible(false);
            onUpdate()
        } catch (err) {
            let errMessage = "";
            if (err instanceof Error) {
                errMessage = err.message;
            }
            console.log(errMessage);
            message.error(errMessage)
        }
        setIsLoading(false)
    }

    useEffect(() => {
        if (isVisible) {
            fetchSubjectAreas()
        }
    }, [isVisible])

    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const onFinish = values => {
        console.log('Received values of form:', values);
        const item = {
            nameModule: values.nameModule,
            subjectArea: values.subjectArea,
            avatar: url,
            practice: [],
            lectures: [],
            tests: [],
        }
        fetchCreateModule(item)
    };

    const listAreas = subAreas.map((item) => {
        return (
            <Option key={item.subjectAreaObj} value={item.subjectAreaObj}>{item.subjectArea}</Option>
        )
    }) 

    if (isDataLoading || isLoading) {
        return <Loader/>
    } else {
        return (
            <>
            <Modal title="Создание модуля" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form form={form} name="dynamic_form_nest_item" onFinish={onFinish} autoComplete="off">
                    <Form.Item name="nameModule" label="Название модуля" rules={[{ required: true, message: 'Не заполнено название модуля' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="subjectArea" label="Предметная область" rules={[{ required: true, message: 'Не заполнено название модуля' }]}>
                        <Select placeholder="Select subject area">
                            {listAreas}
                        </Select>
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
};

export default CreateModule;