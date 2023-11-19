import pytest
from scheduling.models.schedule import Constraint, Schedule, Course
from scheduling.solver.checker import check_availabilities


@pytest.fixture
def mock_schedule_success():
    schedule = Schedule(
        name="mock_schedule",
        n_days=1,
        n_periods=2,
        courses_size=1,
        rooms_size=1,
        curricula_size=0,
        constraints_size=1,
    )
    schedule.courses = [
        Course(
            id="course1",
            teacher_id="teacher1",
            min_working_days=1,
            n_lectures=1,
            n_students=1
        ),
    ]
    schedule.constraints = [
        Constraint(
            course_id="course1",
            day=0,
            day_period=0,
        )
    ]
    return schedule

class TestAvailabityChecker:
    def test_check_availability_pass(self, mock_schedule_success):
        matrix_solution = [[-1, 0]]
        schedule = mock_schedule_success
        score = check_availabilities(matrix_solution, schedule)
        assert score == 0

    def test_check_availability_fail(self, mock_schedule_success):
        matrix_solution = [[0, -1]]
        schedule = mock_schedule_success
        score = check_availabilities(matrix_solution, schedule)
        assert score == 1
