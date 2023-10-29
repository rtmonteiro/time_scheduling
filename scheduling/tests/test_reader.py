from scheduling.reader.reader import read_constraint, read_course, read_curriculum, read_room


class TestGoodReading:
    def test_read_constraint(self):
        constraint = read_constraint("c0211 0 2 ")
        assert constraint.course_id == "c0211"
        assert constraint.day == 0
        assert constraint.day_period == 2

    def test_read_curriculum_long(self):
        curriculum = read_curriculum("q048 6 c0323 c0327 c0076 c0279 c0074 c0480 ")
        assert curriculum.id == "q048"
        assert len(curriculum.members) == 6

    def test_read_curriculum_short(self):
        curriculum = read_curriculum("q068 1 c0304 ")
        assert curriculum.id == "q068"
        assert len(curriculum.members) == 1

    def test_read_room(self):
        room = read_room("r36 42")
        assert room.id == "r36"
        assert room.capacity == 42

    def test_read_course(self):
        course = read_course("c0131 t000 3 2 150")
        assert course.id == "c0131"
        assert course.teacher_id == "t000"
        assert course.n_lectures == 3
        assert course.min_working_days == 2
        assert course.n_students == 150
