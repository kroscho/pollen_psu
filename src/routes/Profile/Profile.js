import React, {useContext, useState} from "react";
import { Context } from "../../index"
import { Button, Table } from "react-bootstrap";
import { Col, Divider, Row } from "antd";
import ProfileEdit from "../../components/Course/ModalForms/ProfileEdit";


const Profile = () => {
    
    const {userStore} = useContext(Context);
    const [isProfileEditFormVisible, setIsProfileEditFormVisible] = useState(false)
    const user = userStore.User;

    const handleEditProfile = () => {
        setIsProfileEditFormVisible(true)
    }

    return (
        <div className="contain">
            <Row>
                <Col xs={9}>
                    <Divider style={{color: 'rgb(24 144 255)', fontSize: '20px'}} orientation="left">Мои данные</Divider>
                    <Table striped bordered>
                        <tbody>
                            <tr>
                                <th>Имя</th>
                                <td>{user.firstName}</td>
                            </tr>
                            <tr>
                                <th>Фамилия</th>
                                <td>{user.lastName}</td>
                            </tr>
                            <tr>
                                <th>Роль</th>
                                <td>{user.role}</td>
                            </tr>
                            <tr>
                                <th>Email</th>
                                <td>{user.email}</td>
                            </tr>
                        </tbody>
                    </Table>
                    <Button onClick={handleEditProfile} style={{marginLeft: "5px"}} variant="outline-secondary">Редактировать профиль</Button>
                </Col>
            </Row>
            <ProfileEdit isVisible={isProfileEditFormVisible} setIsVisible={setIsProfileEditFormVisible}></ProfileEdit>
        </div>
    );
}

export default Profile;