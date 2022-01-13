import React, { useState } from "react";
import { Form, Input, Button } from "antd";
import { Layout } from "antd";
import { auth } from "../../services/firebase";
import "./styles.css";

const { Content } = Layout;

const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 16 },
};

function LoginForm({ onSubmit }: any) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [typeLog, setTypeLog] = useState(true)

  const handleRegIn = () => {
    return auth.createUserWithEmailAndPassword(email, password)
      .catch((error) => { console.log(error) });
  };

  const handleSubmit = () => {
    onSubmit(email, password);
  };

  if (typeLog) {
    return (
      <Content>
        <div className="loginContainer">
          <Form
            {...layout}
            name="basic"
            initialValues={{ remember: true }}
            onFinish={handleSubmit}
          >
            <Form.Item
              label="Email"
              name="email"
              rules={[{ required: true, message: "Введите почту" }]}
            >
              <Input
                required
                type={"email"}
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </Form.Item>
  
            <Form.Item
              label="Пароль"
              name="password"
              rules={[{ required: true, message: "Введите пароль" }]}
            >
              <Input.Password
                required
                type={"password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </Form.Item>
  
            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Войти
              </Button>
              <div>Или <a onClick={() => setTypeLog(!typeLog)} >зарегистрироваться сейчас!</a></div>
            </Form.Item>
          </Form>
        </div>
      </Content>
    );
  }
  else {
    return (
      <Content>
        <div className="loginContainer">
          <Form
            {...layout}
            name="basic"
            initialValues={{ remember: true }}
            onFinish={handleRegIn}
          >
            <Form.Item
              label="Email"
              name="email"
              rules={[{ required: true, message: "Введите почту" }]}
            >
              <Input
                required
                type={"email"}
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </Form.Item>
  
            <Form.Item
              label="Пароль"
              name="password"
              rules={[{ required: true, message: "Введите пароль" }]}
            >
              <Input.Password
                required
                type={"password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </Form.Item>
  
            <Form.Item {...tailLayout}>
              <Button type="primary" htmlType="submit">
                Зарегистрироваться
              </Button>
              <div>Или <a onClick={() => setTypeLog(!typeLog)} >войдите сейчас!</a></div>
            </Form.Item>
          </Form>
        </div>
      </Content>
    );
  }
}

export default LoginForm;
