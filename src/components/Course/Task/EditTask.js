import React from 'react';
import 'antd/dist/antd.css';
import { Form, Input, Space, Checkbox, Button } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import { TEXT_TASK_TYPE } from '../../../utils/consts';

const EditTask = ({field, form, tasks}) => {

    if (form.getFieldsValue().tasks || tasks) {
        if (form.getFieldsValue().tasks) {
            tasks = form.getFieldsValue().tasks
        }
        let questionType = ""
        if (tasks[field.key] && tasks[field.key].type) {
            questionType = tasks[field.key].type
        } else {
            questionType = TEXT_TASK_TYPE
        }
        console.log("questionType: ", questionType)
        if (questionType !== TEXT_TASK_TYPE) {
            return (
                <Form.List name={[field.name, 'answers']}>
                    {(fields = fields[field.key].answers, { add, remove }) => (
                    <>
                        {fields.map((fld, index) => (
                        <Space key={fld.key} style={{display: 'flex', justifyContent: 'center'}} align="baseline">
                            <Form.Item
                            {...fld.restField}
                            name={[fld.name, 'answer']}
                            label={"Ответ " + index + ":"} 
                            rules={[{ required: true, message: 'Не заполнен ответ' }]}
                            >
                            <Input style={{borderRadius: '10px'}} />
                            </Form.Item>
                            <Form.Item
                                name={[fld.name, 'correct']}
                                valuePropName="checked"
                            >
                                <Checkbox>Верный</Checkbox>
                            </Form.Item>
                            <MinusCircleOutlined onClick={() => remove(fld.name)} />
                        </Space>
                        ))}
                        <Form.Item>
                        <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                            Добавить ответ
                        </Button>
                        </Form.Item>
                    </>
                    )}
                </Form.List>
            );
        } else {
            return null
        }
    } else {
        return null
    }
};


export default EditTask;