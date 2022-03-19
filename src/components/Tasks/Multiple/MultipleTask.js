import React from "react";
import { Form, Checkbox, Space } from "antd";

const MultipleTask = (props) => {
    
    function onChange(checkedValues) {
        console.log('checked = ', checkedValues);
    }

    const listAnswers = props.task.answers.map((item) => {
        return (
            <Checkbox key={item.id} value={item.answer}>{item.answer}</Checkbox>
        )
    })
    
    return (
        <Form.Item 
            label={props.task.question} 
            required tooltip="This is a required field"
            style={{borderBottomStyle: "solid", color: "rgb(216 162 162 / 13%)"}}
        >
            <Checkbox.Group style={{ width: '100%' }} onChange={onChange}>
                <Space direction="vertical">
                    {listAnswers}
                </Space>
            </Checkbox.Group>
        </Form.Item>
    )
}

export default MultipleTask;