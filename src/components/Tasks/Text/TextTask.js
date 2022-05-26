import React from "react";
import { Form, Input } from "antd";

const TextTask = ({field, task}) => {
    return (
        <Form.Item
            name={[field.name, 'answer']}
            label={task.question} 
            required tooltip="This is a required field"
            style={{borderBottomStyle: "solid", color: "rgb(216 162 162 / 13%)"}}
            rules={[{ required: true, message: 'Не заполнен ответ' }]}
        >
            <Input placeholder="input placeholder" />
        </Form.Item>
    )
}

export default TextTask;