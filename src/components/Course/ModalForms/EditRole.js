import React, { useContext, useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button, Form, Input, message, Select } from 'antd';
import { Context } from '../../..';
import { useFetching } from '../../hooks/useFetching';
import TestingApi from '../../../API/TestingApi';
import Loader from '../../UI/Loader/Loader';
import ErrorMessage from '../../UI/Messages/ErrorMessage';

const { Option } = Select;

const RoleEdit = ({onUpdateUsers, user, isVisible, setIsVisible}) => {
    const {userStore} = useContext(Context)
    const [form] = Form.useForm();

    const [fetchEditRole, isEditLoading, editError] = useFetching(async () => {
        let response = await TestingApi.editRole(userStore.CurNewUser);
        if (response.data === "ok") {
            message.success('Роль пользователя изменена успешно');
            onUpdateUsers()
            setIsVisible(false)
        }
        userStore.setCurNewUser({})
        console.log(response.data)
    })

    const handleOk = () => {
        setIsVisible(false);
    };

    const handleCancel = () => {
        setIsVisible(false);
    };

    const onFinish = values => {
        values["uid"] = user.uid
        values["userObj"] = user.userObj
        console.log('Received values of form:', values);
        userStore.setCurNewUser(values)
        fetchEditRole()
    };

    const onRoleChange = (value) => {
        console.log(value)
    }

    const View = () => {
        return (
            <>
            <Modal title="Редактирование роли" visible={isVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form 
                    form={form} 
                    name="dynamic_form_nest_item" 
                    onFinish={onFinish} 
                    autoComplete="off"
                    initialValues={{
                        ["firstName"]: user.firstName,
                        ["lastName"]: user.lastName,
                        ["role"]: user.role,
                        ["email"]: user.email,
                    }}
                >
                    <Form.Item name="firstName" label="Имя">
                        <Input disabled/>
                    </Form.Item>
                    <Form.Item name="lastName" label="Фамилия">
                        <Input disabled/>
                    </Form.Item>
                    <Form.Item
                        name="role"
                        label="Роль"
                        rules={[{required: true}]}
                        >
                        <Select
                            placeholder="Select a option and change input text above"
                            onChange={onRoleChange}
                            allowClear
                        >
                            <Option value="student">student</Option>
                            <Option value="admin">admin</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="email" label="Email">
                        <Input disabled/>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Подтвердить изменения
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
            </>
        );
    }

    const spinner = isEditLoading ? <Loader/> : null;
    const errorMessage = editError ? <ErrorMessage message={editError} /> : null;
    const content = !(isEditLoading || editError) ? <View/> : null;

    return (
        <>
            {spinner}
            {errorMessage}
            {content}
        </>
    )
};

export default RoleEdit;