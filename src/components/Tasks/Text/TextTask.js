import React from "react";
import { Form, Input } from "antd";

const TextTask = (props) => {
    return (
        <Form.Item 
            label={props.task.question} 
            required tooltip="This is a required field"
            style={{borderBottomStyle: "solid", color: "rgb(216 162 162 / 13%)"}}
        >
            <Input placeholder="input placeholder" />
        </Form.Item>
    )
}

export default TextTask;