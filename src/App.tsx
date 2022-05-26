import React, { useState, useEffect, useContext } from "react";
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
import Testing from "./routes/Testing/Testing";
import { ADD_ROUTE, ALLERGENS_ROUTE, ARCHIVE_ROUTE, COURSE_INFO_ROUTE, COURSE_LECTIONS_ROUTE, COURSE_LECTURE_ROUTE, COURSE_LITERATURE_ROUTE, COURSE_TESTS_ROUTE, COURSE_TESTS_TEST_EDIT_ROUTE, COURSE_TESTS_TEST_ROUTE, COURSE_TESTS_TEST_VARIANTS_ROUTE, LOGIN_ROUTE, MAIN_ROUTE, PROFILE_ROUTE, SEARCH_ROUTE, TESTING_ALL_COURSES_ROUTE, TESTING_COURSES_ROUTE, TESTING_INFO_ROUTE, TESTING_MATERIALS_ROUTE, TESTING_ROUTE, TESTING_TESTS_ROUTE, TESTS_TEST_ATTEMPT_ROUTE, TESTS_TEST_ROUTE, VIEW_ROUTE } from "./utils/consts";
import { Context } from ".";

const { Header, Footer, Content } = Layout;

const App = () => {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const {services} = useContext(Context);

  const handleSignIn = (email: string, password: string) => {
    return auth.signInWithEmailAndPassword(email, password).then((user) => {
      setUser(user);
      console.log("user: ", user.user?.email)
      return history.push(SEARCH_ROUTE);
    });
  };

  const logOut = () => {
    return auth.signOut().then(() => {
      return history.push(LOGIN_ROUTE);
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
      case MAIN_ROUTE:
        return "1";
      case ALLERGENS_ROUTE:
        return "2";
      case ADD_ROUTE:
        return "3";
      case VIEW_ROUTE:
        return "4";
      case ARCHIVE_ROUTE:
        return "5";
      case SEARCH_ROUTE:
        return "6";
      case TESTING_ROUTE:
        return "7";
      case PROFILE_ROUTE:
        return "8";
      default:
        return "1";
    }
  };

  const menuItems = services.MenuApp.map((item: any) => {
    return (
      <Menu.Item key={item.id}>
        <Link to={item.link}>{item.name}</Link>
      </Menu.Item>
    )
  })

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
              {menuItems}
            </Menu>
            {user && (
              <Button type="link" onClick={logOut}>
                Выйти
              </Button>
            )}
          </Header>
          <Switch>
            <Route
              path={LOGIN_ROUTE}
              exact
              render={() => (
                <Content>
                  <LoginForm onSubmit={handleSignIn} />
                </Content>
              )}
            />

            <Route path={VIEW_ROUTE} exact component={ViewData} />

            <ProtectedRoute
              exact
              path={ADD_ROUTE}
              user={user}
              loading={loading}
              component={AddData}
            />

            <ProtectedRoute
              exact
              path={SEARCH_ROUTE}
              user={user}
              loading={loading}
              component={Search}
            />

            <ProtectedRoute
              exact
              path={TESTING_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <Route exact path={ARCHIVE_ROUTE} component={Archive} />
            <Route exact path={ALLERGENS_ROUTE} component={Allergens} />
            
            <Route 
              exact 
              path={PROFILE_ROUTE}
              user={user}
              component={Profile} 
            />

            <ProtectedRoute
              exact
              path={TESTING_COURSES_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <ProtectedRoute
              exact
              path={TESTING_ALL_COURSES_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <ProtectedRoute
              exact
              path={TESTING_TESTS_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <ProtectedRoute
              exact
              path={TESTING_INFO_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <ProtectedRoute
              exact
              path={TESTING_MATERIALS_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <ProtectedRoute
              exact
              path={TESTS_TEST_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
            />

            <ProtectedRoute
              exact
              path={TESTS_TEST_ATTEMPT_ROUTE}
              user={user}
              loading={loading}
              component={Testing}
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
