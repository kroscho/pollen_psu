import React from "react";
import { Form, Checkbox, Space } from "antd";

const MultipleTask = ({task, field}) => {
    
    function onChange(checkedValues) {
        console.log('checked = ', checkedValues);
    }

    const listAnswers = task.answers.map((item, ind) => {
        return (
            <Checkbox key={ind} value={item.answer}>{item.answer}</Checkbox>
        )
    })
    
    return (
        <Form.Item 
            name={[field.name, "answer"]}
            label={task.question}
            rules={[{ required: true, message: 'Не заполнен ответ' }]}
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