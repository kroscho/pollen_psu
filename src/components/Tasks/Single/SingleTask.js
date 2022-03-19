import React, { useState } from "react";
import { Form, Radio, Space } from "antd";

const SingleTask = (props) => {
    
    const [value, setValue] = useState('')
    
    const onChange = (e) => {
        setValue(e.target.value)
    };

    const listAnswers = props.task.answers.map((item) => {
        return (
            <Radio key={item.id} value={item.id}>{item.answer}</Radio>
        )
    })
    
    return (
        <Form.Item 
            label={props.task.question} 
            required tooltip="This is a required field"
            style={{borderBottomStyle: "solid", color: "rgb(216 162 162 / 13%)"}}
        >
            <Radio.Group onChange={onChange} value={value}>
                <Space direction="vertical">
                {listAnswers}
                </Space>
            </Radio.Group>
        </Form.Item>
    )
}

export default SingleTask;