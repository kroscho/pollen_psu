import React, { useState } from "react";
import { Form, Radio, Space } from "antd";

const SingleTask = ({task}) => {
    
    const [value, setValue] = useState('')
    let listAnswers = []

    const logicalAnswers = [{"answer": "Да"}, {"answer": "Нет"}]

    const onChange = (e) => {
        setValue(e.target.value)
    };

    if (task.answers.length === 0) {
        listAnswers = logicalAnswers.map((item, ind) => {
            return (
                <Radio key={ind} value={ind}>{item.answer}</Radio>
            )
        })
    } else {
        listAnswers = task.answers.map((item, ind) => {
            return (
                <Radio key={ind} value={ind}>{item.answer}</Radio>
            )
        })
    }
    
    return (
        <Form.Item 
            label={task.question} 
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