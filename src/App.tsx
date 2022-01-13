import React, { useState, useEffect } from "react";
import { Router, Switch, Route, Link } from "react-router-dom";
import { Layout, Button, Menu } from "antd";
import "antd/dist/antd.css";
import 'bootstrap/dist/css/bootstrap.css';
import MainPage from "./routes/MainPage";
import AddData from "./routes/AddData/AddData";
import Search from './routes/Search/Search';
import { auth } from "./services/firebase";
import ViewData from "./routes/ViewData/ViewData";
import history from "./services/history";
import { SpeciesContextProvider } from "./services/speciesContext";
import LoginForm from "./routes/LoginForm/LoginForm";
import ProtectedRoute from "./routes/ProtectedRoute";
import "./App.css";
import Archive from "./routes/Archive/Archive";
import Allergens from "./routes/Allergens/Allergens";
import Profile from "./routes/Profile/Profile"

const { Header, Footer, Content } = Layout;

const App = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const handleSignIn = (email: string, password: string) => {
    return auth.signInWithEmailAndPassword(email, password).then((user) => {
      setUser(user);
      console.log("user: ", user.user?.email)
      return history.push("/add");
    });
  };

  const logOut = () => {
    return auth.signOut().then(() => {
      return history.push("/login");
    });
  };

  useEffect(() => {
    console.log(history);
    auth.onAuthStateChanged((user) => {
      setUser(user);
      setLoading(false);
    });
  }, []);

  const getDefaultKey = () => {
    switch (history.location.pathname) {
      case "/":
        return "1";
      case "/allergens":
        return "2";
      case "/add":
        return "3";
      case "/view":
        return "4";
      case "/archive":
        return "5";
      case "/search":
        return "6";
      case "/profile":
        return "7";
      default:
        return "1";
    }
  };
  return (
    <SpeciesContextProvider>
      <Router history={history}>
        <Layout style={{ minHeight: "100vh" }}>
          <Header className="mainHeader">
            <Menu
              theme="dark"
              mode="horizontal"
              //@ts-ignore
              defaultSelectedKeys={getDefaultKey()}
            >
              {/* defaultSelectedKeys={["1"]} */}
              <Menu.Item key="1">
                <Link to="/">Главная</Link>
              </Menu.Item>
              <Menu.Item key="2">
                <Link to="/allergens">Аллергены</Link>
              </Menu.Item>
              <Menu.Item key="3">
                <Link to="/add">Добавление</Link>
              </Menu.Item>
              <Menu.Item key="4">
                <Link to="/view">Мониторинг</Link>
              </Menu.Item>
              <Menu.Item key="5">
                <Link to="/archive">Архив</Link>
              </Menu.Item>
              <Menu.Item key="6">
                <Link to="/search">Поиск</Link>
              </Menu.Item>
              {user && (
                <Menu.Item key="7">
                  <Link to="/profile">Профиль</Link>
                </Menu.Item>
              )}
            </Menu>
            {user && (
              <Button type="link" onClick={logOut}>
                Выйти
              </Button>
            )}
          </Header>
          <Switch>
            <Route
              path="/login"
              exact
              render={() => (
                <Content>
                  <LoginForm onSubmit={handleSignIn} />
                </Content>
              )}
            />

            <Route path="/view" exact component={ViewData} />

            <ProtectedRoute
              exact
              path="/add"
              user={user}
              loading={loading}
              component={AddData}
            />

            <ProtectedRoute
              exact
              path="/search"
              user={user}
              loading={loading}
              component={Search}
            />

            <Route exact path="/archive" component={Archive} />
            <Route exact path="/allergens" component={Allergens} />
            
            <Route 
              exact 
              path="/profile" 
              user={user}
              component={Profile} 
            />
            

            <Route path="/" exact component={MainPage} />
          </Switch>
          <Footer style={{ textAlign: "center" }}>PSU, 2020</Footer>
        </Layout>
      </Router>
    </SpeciesContextProvider>
  );
}

export default App;
