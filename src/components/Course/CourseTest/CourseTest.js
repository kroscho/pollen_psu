import React, { useContext } from "react";
import 'antd/dist/antd.css';
import { Context } from "../../..";
import { Button} from "react-bootstrap"
import { Divider, Form } from "antd";
import SingleTask from "../../Tasks/Single/SingleTask";
import MultipleTask from "../../Tasks/Multiple/MultipleTask";
import TextTask from "../../Tasks/Text/TextTask";
import { LOGICAL_TASK_TYPE, MULTIPLE_TASK_TYPE, SINGLE_TASK_TYPE } from "../../../utils/consts";

const CourseTest = () => {
    const {userStore} = useContext(Context)
    const curTest = userStore.CurTest;
    const [form] = Form.useForm();
    let listTasks = []

    if (curTest.tasks) {
        listTasks = curTest.tasks.map((item, ind) => {
            if (item.type === SINGLE_TASK_TYPE || item.type === LOGICAL_TASK_TYPE) {
                return <SingleTask key={ind} task={item}></SingleTask>
            }
            else if (item.type === MULTIPLE_TASK_TYPE) {
                return <MultipleTask key={ind} task={item}></MultipleTask>
            }
            else {
                return <TextTask key={ind} task={item}></TextTask>
            }
        })
    }

    const onFinish = values => {
        console.log('Received values of form:', values);
    };

    if (curTest.tasks) {
        return (
            <Form
                style={{margin: "0 20%"}}
                form={form}
                layout="vertical"
                onFinish={onFinish} 
                autoComplete="off"
            >
                <Divider orientation="center">{curTest.nameTest}</Divider>
                {listTasks}
                <Form.Item>
                    <Button type="primary">Завершить тест</Button>
                </Form.Item>
            </Form>
        )
    } else {
        return (
            <Divider orientation="center">Заданий нет</Divider>
        )
    }
}

export default CourseTest;