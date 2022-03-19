import React, { useContext } from "react";
import 'antd/dist/antd.css';
import { Context } from "../../..";
import { Button} from "react-bootstrap"
import { Divider, Form } from "antd";
import SingleTask from "../../Tasks/Single/SingleTask";
import MultipleTask from "../../Tasks/Multiple/MultipleTask";
import TextTask from "../../Tasks/Text/TextTask";

const CourseTest = () => {
    const {userStore} = useContext(Context)
    const curVariant = userStore.CurVariant;
    const curTest = userStore.CurTest;

    let listTasks = []

    if (curVariant.tasks) {
        listTasks = curVariant.tasks.map((item) => {
            if (item.type === "single" || item.type === "truefalse") {
                return <SingleTask key={item.id} task={item}></SingleTask>
            }
            else if (item.type === "multiple") {
                return <MultipleTask key={item.id} task={item}></MultipleTask>
            }
            else {
                return <TextTask key={item.id} task={item}></TextTask>
            }
        })
    }

    const [form] = Form.useForm();

    if (curVariant.tasks) {
        return (
            <Form
                style={{margin: "0 20%"}}
                form={form}
                layout="vertical"
                >
                <Divider orientation="center">{curTest.name}</Divider>
                <Divider orientation="left">{curVariant.name}</Divider>
                {listTasks}
                <Form.Item>
                    <Button type="primary">Завершить тест</Button>
                </Form.Item>
            </Form>
        )
    } else {
        return (
            <Divider orientation="center">Тест не выбран</Divider>
        )
    }
}

export default CourseTest;