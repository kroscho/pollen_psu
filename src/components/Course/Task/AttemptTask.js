import React from 'react';
import 'antd/dist/antd.css';
import { Form, Input, Space, Checkbox } from 'antd';
import { TEXT_TASK_TYPE } from '../../../utils/consts';

const AttemptTask = ({field, tasks}) => {    
    let questionType = ""
    if (tasks[field.key] && tasks[field.key].type) {
        questionType = tasks[field.key].type
    } else {
        questionType = TEXT_TASK_TYPE
    }

    const getStyleInput = (answ) => {
        let styleInput = {borderRadius: '10px', borderColor: "black"}
        if (answ?.correctByUser == undefined) {
            return styleInput
        }
        styleInput = answ?.correctByUser ? {borderRadius: '10px', borderColor: "green", borderWidth: "medium"} : {borderRadius: '10px', borderColor: "red", borderWidth: "medium"};
        return styleInput
    }

    return (
        <Form.List name={[field.name, 'answers']}>
            {(fields = fields[field.key].answers) => (
                <>
                    {fields.map((fld, index) => (
                    <Space key={fld.key} style={{display: 'flex', justifyContent: 'center'}} align="baseline">
                        <Form.Item
                        {...fld.restField}
                        name={[fld.name, 'answer']}
                        label={"Ответ " + index + ":"} 
                        >
                        <Input style={getStyleInput(tasks[field.key].answers[index])} />
                        </Form.Item>
                    </Space>
                    ))}
                    <Form.Item>
                    </Form.Item>
                </>
            )}
        </Form.List>
    )
};


export default AttemptTask;