import React, { useState } from "react";
import { Form, Input, Button } from "antd";
import { Layout } from "antd";
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
  const handleSubmit = () => {
    onSubmit(email, password);
  };
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
          </Form.Item>
        </Form>
      </div>
    </Content>
  );
}

export default LoginForm;
