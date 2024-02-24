class AuthRoutes:
    REGISTER = "/register"
    AUTH = "/auth"
    REFRESH = "/refresh"
    LOGOUT = "/logout"


class TaskRoutes:
    CREATE_TASK = "/task/create"
    UPDATE_TASK = "/task/update"
    GET_TASK_BY_ID = "/task/{id}"
    GET_TASK_BY_COURSE_ID = "/task/get_by_course_id"
    REMOVE_TASK = "/task/remove"


class CourseRoutes:
    CREATE_COURSE = "/course"
    GET_COURSES = "/course"
    GET_COURSE_BY_ID = "/course/{id}"
    ENROLL = "/course/{course_id}/enroll"


class RepositoryRoutes:
    CREATE_REPOSITORY = "/repository"
    GET_REPOSITORY = "/repository/{id}"
