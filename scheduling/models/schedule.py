from json import JSONEncoder


class Schedule:
    def __init__(
        self,
        name: str,
        n_days,
        n_periods,
        courses_size,
        rooms_size,
        curricula_size,
        constraints_size,
    ):
        self.name = name
        self.n_days = int(n_days)
        self.n_periods = int(n_periods)
        self.courses_size = int(courses_size)
        self.rooms_size = int(rooms_size)
        self.curricula_size = int(curricula_size)
        self.constraints_size = int(constraints_size)
        self.courses: list[Course] = []
        self.rooms: list[Room] = []
        self.curricula: list[Curriculum] = []

    def __str__(self):
        return f"Schedule({self.name}, {self.n_days}, {self.n_periods})"
    
    def toJson(self) -> str:
        return JSONEncoder().encode(self.__dict__())
    

class Assignment:
    def __init__(self, 
                 course: str, 
                 room: str,
                 day: int,
                 period: int) -> None:
        self.course_id = course
        self.room_id = room
        self.day = day
        self.period = period
    
    def __str__(self) -> str:
        return f"{self.course_id} {self.room_id} {self.day} {self.period}"


class Course:
    def __init__(self, id, teacher_id, n_lectures, min_working_days, n_students):
        self.id = id
        self.teacher_id = teacher_id
        self.n_lectures = int(n_lectures)
        self.min_working_days = int(min_working_days)
        self.n_students = int(n_students)
        self.constraints: list[Constraint] = []

    def __eq__(self, __value: str) -> bool:
        if isinstance(__value, str):
            return self.id == __value
        return False


class Room:
    def __init__(self, id: str, capacity: str):
        self.id = id
        self.capacity = int(capacity)


    def __eq__(self, __value: str) -> bool:
        if isinstance(__value, str):
            return self.id == __value
        return False


class Curriculum:
    def __init__(self, id: str, members: list[str]):
        self.id = id
        self.members = [member if '\n' not in member else member.split('\n')[0] for member in members]


class Constraint:
    def __init__(self, day: str, day_period: str):
        self.day = int(day)
        self.day_period = int(day_period)
