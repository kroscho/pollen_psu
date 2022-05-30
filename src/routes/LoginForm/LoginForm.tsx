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

function LoginForm({ onSignIn, onRegIn, errorMessage, setErrorMessage }: any) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [typeLog, setTypeLog] = useState(true)

  const handleSign = () => {
    onSignIn(email, password);
  };

  const handleReg = () => {
    const userObj = {email: email, password: password, firstName: firstName, lastName: lastName}
    onRegIn(userObj);
  };

  const onChangeTypeLog = () => {
    setTypeLog(!typeLog)
    setErrorMessage("")
  }

  if (typeLog) {
    return (
      <Content>
        <div className="loginContainer">
          <Form
            {...layout}
            name="basic"
            initialValues={{ remember: true }}
            onFinish={handleSign}
          >
            <Form.Item 
              name="error"
              style={{color: 'red', justifyContent: 'flex-end'}}
            >
              {errorMessage}
            </Form.Item>
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
              <div>Или <a onClick={() => onChangeTypeLog()} >зарегистрироваться сейчас!</a></div>
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
            onFinish={handleReg}
          >
             <Form.Item 
              name="error"
              style={{color: 'red', justifyContent: 'flex-end'}}
            >
              {errorMessage}
            </Form.Item>
            <Form.Item
              label="Имя"
              name="firstName"
              rules={[{ required: true, message: "Введите имя" }]}
            >
              <Input
                required
                type={"firstname"}
                value={firstName}
                onChange={(event) => setFirstName(event.target.value)}
              />
            </Form.Item>
            <Form.Item
              label="Фамилия"
              name="lastName"
              rules={[{ required: true, message: "Введите фамилию" }]}
            >
              <Input
                required
                type={"lastName"}
                value={lastName}
                onChange={(event) => setLastName(event.target.value)}
              />
            </Form.Item>
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
              <div>Или <a onClick={() => onChangeTypeLog()} >войдите сейчас!</a></div>
            </Form.Item>
          </Form>
        </div>
      </Content>
    );
  }
}

export default LoginForm;
