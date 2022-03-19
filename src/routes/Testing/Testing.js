import React, { useContext } from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { Layout, Menu } from 'antd';
import { Router, Switch, Route, Link } from "react-router-dom";
import ListCourses from '../../components/ListCourse/ListCourses';
import { UserOutlined } from '@ant-design/icons';
import history from '../../services/history';
import { Context } from '../..';
import { COURSE_INFO_ROUTE, COURSE_LECTIONS_ROUTE, COURSE_LITERATURE_ROUTE, COURSE_TESTS_ROUTE, COURSE_TESTS_TEST_ROUTE, TESTING_COURSES_ROUTE, TESTING_ROUTE } from '../../utils/consts';
import { isMenuCourses } from '../../components/utils/testing';
import CourseInfo from '../../components/Course/CourseInfo/CourseInfo';
import CourseTests from '../../components/Course/CourseTests/CourseTests';
import CourseTest from '../../components/Course/CourseTest/CourseTest';

const { Header, Content, Sider } = Layout;

const Testing = () => {
    
    const {services, userStore} = useContext(Context)

    const curCourse = userStore.CurCourse;
    console.log(curCourse.title)
    const menuItems = isMenuCourses() ? services.MenuTesting : services.MenuCourse;
    const menuItemsList = menuItems.map((item) => {
        return (
            <Menu.Item key={item.id} icon={<UserOutlined />}>
                <Link to={item.link}>{item.name}</Link>
            </Menu.Item>
        )
    })

    const getDefaultKey = () => {
        switch (history.location.pathname) {
            case TESTING_ROUTE:
                return "0";
            case TESTING_COURSES_ROUTE:
                return "1";
            case COURSE_INFO_ROUTE:
                return "1";
            case COURSE_LECTIONS_ROUTE:
                return "2";
            case COURSE_TESTS_ROUTE:
                return "3";
            case COURSE_LITERATURE_ROUTE:
                return "4";
            case COURSE_TESTS_TEST_ROUTE:
                return "3";
            default:
                return "0";
        }
    };

    return (
        <Router history={history}>
            <Layout>
                <Sider
                breakpoint="lg"
                collapsedWidth="0"
                onBreakpoint={broken => {
                    console.log(broken);
                }}
                onCollapse={(collapsed, type) => {
                    console.log(collapsed, type);
                }}
                >
                    <div className="logo">
                        {isMenuCourses()
                            ? ""
                            : curCourse.title 
                        }
                    </div>
                    <Menu theme="dark" mode="inline" defaultSelectedKeys={getDefaultKey()}>
                        {menuItemsList}
                    </Menu>
                </Sider>
                <Layout>
                    <Header className="site-layout-sub-header-background" style={{ padding: 0 }} />
                    <Content style={{ margin: '24px 16px 0' }}>
                        <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
                            <Switch>
                                <Route axact path={COURSE_INFO_ROUTE}>
                                    <CourseInfo/>
                                </Route>
                                <Route exact path={COURSE_TESTS_ROUTE}>
                                    <CourseTests/>
                                </Route>
                                <Route exact path={COURSE_LECTIONS_ROUTE}>
                                    <ListCourses/>
                                </Route>
                                <Route exact path={COURSE_LITERATURE_ROUTE}>
                                    <ListCourses/>
                                </Route>
                                <Route exact path={TESTING_COURSES_ROUTE}>
                                    <ListCourses/>
                                </Route>
                                <Route exact path={COURSE_TESTS_TEST_ROUTE}>
                                    <CourseTest/>
                                </Route>
                            </Switch>
                        </div>
                    </Content>
                </Layout>
            </Layout>
        </Router>
    )
}

export default Testing;