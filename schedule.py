class Schedule:
    def __init__(
        self,
        name,
        n_days,
        n_periods,
    ):
        self.name = name
        self.n_days = int(n_days)
        self.n_periods = int(n_periods)
        self.courses = []
        self.rooms = []
        self.curricula = []
        self.constraints = []

    def __str__(self):
        return f"Schedule({self.name}, {self.n_days}, {self.n_periods})"


class Course:
    def __init__(self, id, teacher, n_lectures, min_working_days, n_students):
        self.id = id
        self.teacher = teacher
        self.n_lectures = int(n_lectures)
        self.min_working_days = int(min_working_days)
        self.n_students = int(n_students)


class Room:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = int(capacity)


class Curricula:
    def __init__(self, id, members):
        self.id = id
        self.members = members


class Constraint:
    def __init__(self, course_id, day, day_period):
        self.course_id = course_id
        self.day = day
        self.day_period = day_period
