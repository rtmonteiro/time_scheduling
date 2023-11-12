from json import JSONEncoder


class Schedule:
    def __init__(
        self,
        name,
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
        self.constraints: list[Constraint] = []

    def __str__(self):
        return f"Schedule({self.name}, {self.n_days}, {self.n_periods})"
    
    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "n_days": self.n_days,
            "n_periods": self.n_periods,
            "courses_size": self.courses_size,
            "rooms_size": self.rooms_size,
            "curricula_size": self.curricula_size,
            "constraints_size": self.constraints_size,
            "courses": [course.__dict__() for course in self.courses],
            "rooms": [room.__dict__() for room in self.rooms],
            "curricula": [curriculum.__dict__() for curriculum in self.curricula],
            "constraints": [constraint.__dict__() for constraint in self.constraints]
        }
    
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
    
    def __dict__(self) -> dict:
        return {
            "course_id": self.course_id,
            "room_id": self.room_id,
            "day": self.day,
            "period": self.period
        }

class Course:
    def __init__(self, id, teacher_id, n_lectures, min_working_days, n_students):
        self.id = id
        self.teacher_id = teacher_id
        self.n_lectures = int(n_lectures)
        self.min_working_days = int(min_working_days)
        self.n_students = int(n_students)

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "n_lectures": self.n_lectures,
            "min_working_days": self.min_working_days,
            "n_students": self.n_students
        }


class Room:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = int(capacity)
    
    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "capacity": self.capacity
        }

    def __eq__(self, __value: str) -> bool:
        if isinstance(__value, str):
            return self.id == __value
        return False


class Curriculum:
    def __init__(self, id, members):
        self.id = id
        self.members = members
    
    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "members": self.members
        }


class Constraint:
    def __init__(self, course_id, day, day_period):
        self.course_id = course_id
        self.day = int(day)
        self.day_period = int(day_period)
    
    def __dict__(self) -> dict:
        return {
            "course_id": self.course_id,
            "day": self.day,
            "day_period": self.day_period
        }
