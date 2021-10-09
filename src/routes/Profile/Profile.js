import React, {useContext} from "react";
import { Context } from "../../index"
import { Table } from "react-bootstrap";


const Profile = () => {
    
    const {user} = useContext(Context)

    const listData = user.User.map((item) => {
        return (
            <tr>
                <td>{item.id}</td>
                <td>
                    {Array.isArray(item.data) 
                        ? item.data.map((it) => it + "|     ")
                        : item.data
                    }
                </td>
                
            </tr>
        )
    })

    return (
        <div className="contain">
            <Table striped bordered hover>
                <thead>
                    <tr>
                    <th>#</th>
                    <th>Данные</th>
                    </tr>
                </thead>
                <tbody>
                    {listData}
                </tbody>
            </Table>
        </div>
    );
}

export default Profile;