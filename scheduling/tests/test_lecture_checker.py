import pytest
from scheduling.models.schedule import Course, Schedule
from scheduling.solver.checker import check_lecture_not_schedule, check_course_not_schedule

@pytest.fixture
def mock_schedule_success():
    schedule = Schedule(
        name="mock_schedule",
        n_days=3,
        n_periods=6,
        courses_size=6,
        rooms_size=3,
        curricula_size=3,
        constraints_size=3,
    )
    schedule.courses = [Course(
        id=f"course_{_}",
        teacher_id=f"teacher_{_}",
        n_students=10,
        n_lectures=3,
        min_working_days=2
    ) for _ in range(schedule.courses_size)]
    return schedule


@pytest.fixture
def mock_schedule_failure():
    schedule = Schedule(
        name="mock_schedule",
        n_days=3,
        n_periods=6,
        courses_size=7,
        rooms_size=3,
        curricula_size=3,
        constraints_size=3,
    )
    schedule.courses = [Course(
        id=f"course_{_}",
        teacher_id=f"teacher_{_}",
        n_students=10,
        n_lectures=3,
        min_working_days=2
    ) for _ in range(schedule.courses_size)]
    schedule.courses[5].n_lectures = 4
    return schedule

class TestLectureChecker:
    def test_check_course_not_schedule_success(self, mock_schedule_success):
        matrix = [[0, 0, 0, 1, 1, 1],
                  [2, 2, 2, 3, 3, 3],
                  [4, 4, 4, 5, 5, 5]]
        schedule = mock_schedule_success
        score = check_course_not_schedule(matrix, schedule)
        assert score == 0
    
    def test_check_course_not_schedule_failure(self, mock_schedule_failure):
        matrix = [[0, 0, 0, 1, 1, 1],
                  [2, 2, 2, 3, 3, 3],
                  [4, 4, 4, 5, 5, 5]]
        schedule = mock_schedule_failure
        score = check_course_not_schedule(matrix, schedule)
        assert score == 1

    def test_check_lecture_not_schedule_success(self, mock_schedule_success):
        matrix = [[0, 0, 0, 1, 1, 1],
                  [2, 2, 2, 3, 3, 3],
                  [4, 4, 4, 5, 5, 5]]
        schedule = mock_schedule_success
        score = check_lecture_not_schedule(matrix, schedule)
        assert score == 0
    
    def test_check_lecture_not_schedule_failure(self, mock_schedule_failure):
        matrix = [[0, 0, 0, 1, 1, 1],
                  [2, 2, 2, 3, 3, 3],
                  [4, 4, 4, 5, 5, 5]]
        schedule = mock_schedule_failure
        score = check_lecture_not_schedule(matrix, schedule)
        assert score == 1
