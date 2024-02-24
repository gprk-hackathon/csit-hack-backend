class AuthRoutes:
    REGISTER = "/register"
    AUTH = "/auth"
    REFRESH = "/refresh"
    LOGOUT = "/logout"


class TaskRoutes:
    CREATETASK = "/task/create"
    UPDATETASK = "/task/update"
    GETTASKBYID = "/task/{id}"
    GETTASKBYCOURSEID = "/task/get_by_course_id"
    REMOVETASK = "/task/remove"


class CourseRoutes:
    CREATE_COURSE = "/course"
    GET_COURSES = "/course"
    GET_COURSE_BY_ID = "/course/{id}"
    ENROLL = "/course/{course_id}/enroll"
