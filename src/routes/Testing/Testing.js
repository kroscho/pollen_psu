import React, { useContext } from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { Layout, Menu } from 'antd';
import { Breadcrumb } from 'react-bootstrap'
import { Router, Switch, Route, Link } from "react-router-dom";
import { UserOutlined } from '@ant-design/icons';
import history from '../../services/history';
import { Context } from '../..';
import { COURSE_INFO_ROUTE, COURSE_TESTS_ROUTE, TESTING_INFO_ROUTE, TESTING_MATERIALS_ROUTE, TESTING_ROUTE, TESTING_TESTS_ROUTE, TESTS_TEST_ATTEMPT_ROUTE, TESTS_TEST_ROUTE } from '../../utils/consts';
import CourseInfo from '../../components/Course/CourseInfo/CourseInfo';
import CourseTests from '../../components/Course/CourseTests/CourseTests';
import CourseTest from '../../components/Course/CourseTest/CourseTest';
import CourseTestVariants from '../../components/Course/CourseTestVariants/CourseTestVariants';
import CourseLecture from '../../components/Course/CourseLecture/CourseLecture';

const { Header, Content, Sider } = Layout;

const Testing = () => {
    
    const {services} = useContext(Context)

    const routes = services.Routes[history.location.pathname];

    const menuItems = services.MenuTesting;
    const menuItemsList = menuItems.map((item) => {
        return (
            <Menu.Item key={item.link} icon={<UserOutlined />}>
                <Link to={item.link}>{item.name}</Link>
            </Menu.Item>
        )
    })

    let listRoutes = []

    if (routes) {
        listRoutes = routes.map((item) => {
            if (item.active) {
                return (
                    <Breadcrumb.Item key={item.path} active>{item.title}</Breadcrumb.Item>
                )
            } else {
                return (
                    <Breadcrumb.Item key={item.path} linkAs={Link} linkProps={{ to: item.path }}>
                        {item.title}
                    </Breadcrumb.Item>
                )
            }
        })
    }

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
                    <Menu 
                        theme="dark" 
                        mode="inline" 
                        defaultSelectedKeys={['/']}
                        selectedKeys={[history.location.pathname]}
                    >
                        {menuItemsList}
                    </Menu>
                </Sider>
                <Layout>
                    <Header className="site-layout-sub-header-background" style={{ padding: 0 }} />
                    <Content style={{ margin: '24px 16px 0' }}>
                        <Breadcrumb>
                            {listRoutes}
                        </Breadcrumb>
                        <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
                            <Switch>
                                <Route exact path={TESTING_INFO_ROUTE}>
                                    <CourseInfo/>
                                </Route>
                                <Route exact path={TESTING_TESTS_ROUTE}>
                                    <CourseTests/>
                                </Route>
                                <Route exact path={TESTING_MATERIALS_ROUTE}>
                                    <CourseLecture/>
                                </Route>
                                <Route exact path={TESTS_TEST_ATTEMPT_ROUTE}>
                                    <CourseTest/>
                                </Route>
                                <Route exact path={TESTS_TEST_ROUTE}>
                                    <CourseTestVariants/>
                                </Route>
                                <Route exact path={COURSE_INFO_ROUTE}>
                                    <CourseInfo/>
                                </Route>
                                <Route exact path={COURSE_TESTS_ROUTE}>
                                    <CourseTests/>
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