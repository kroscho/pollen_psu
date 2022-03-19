import history from "../../services/history"
import { TESTING_COURSES_ROUTE, TESTING_ROUTE } from "../../utils/consts"

export const isMenuCourses = () => {
    return  history.location.pathname === TESTING_ROUTE || history.location.pathname === TESTING_COURSES_ROUTE
} 

export const isAdmin = (user) => {
    return user[3].data === "admin"; 
}