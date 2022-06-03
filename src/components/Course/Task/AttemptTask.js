import React from 'react';
import 'antd/dist/antd.css';
import { Form, Input, Space, Checkbox, InputNumber } from 'antd';
import { TEXT_TASK_TYPE } from '../../../utils/consts';
import { getWordAnswer } from '../../utils/testing';

const AttemptTask = ({field, tasks, isCheck}) => {    
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
                        label={getWordAnswer(index)} 
                        >
                        <Input style={getStyleInput(tasks[field.key].answers[index])} />
                        </Form.Item>
                        { questionType === TEXT_TASK_TYPE
                            ?   <Form.Item label="Балл за ответ">
                                    <Form.Item 
                                        rules={[{ required: true, message: 'Не заполнен текст вопроса' }]} 
                                        name={[fld.name, 'score']} 
                                        noStyle
                                    >
                                        <InputNumber min={0} max={1} disabled={!isCheck}/>
                                    </Form.Item>
                                    <span className="ant-form-text"> баллов</span>
                                </Form.Item>
                            :   null
                        }
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