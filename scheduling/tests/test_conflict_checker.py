import pytest
from scheduling.models.schedule import Course, Curriculum, Schedule
from scheduling.solver.checker import check_conflicts

@pytest.fixture
def mock_schedule_success():
    schedule = Schedule(
        name="mock_schedule",
        n_days=1,
        n_periods=1,
        courses_size=2,
        rooms_size=2,
        curricula_size=2,
        constraints_size=0,
    )
    schedule.courses = [Course(
        id=f"course_{_}",
        teacher_id=f"teacher_{_}",
        n_students=10,
        n_lectures=1,
        min_working_days=1
    ) for _ in range(schedule.courses_size)]
    schedule.curricula = [Curriculum(
        id=f"curriculum_0",
        members=[schedule.courses[_].id]
    ) for _ in range(schedule.curricula_size)]
    return schedule


@pytest.fixture
def mock_schedule_fail():
    schedule = Schedule(
        name="mock_schedule",
        n_days=1,
        n_periods=1,
        courses_size=2,
        rooms_size=1,
        curricula_size=1,
        constraints_size=0,
    )
    schedule.courses = [Course(
        id=f"course_{_}",
        teacher_id=f"teacher_0",
        n_students=10,
        n_lectures=1,
        min_working_days=1
    ) for _ in range(schedule.courses_size)]
    schedule.curricula = [Curriculum(
        id=f"curriculum_0",
        members=[c.id for c in schedule.courses]
    )]
    return schedule

@pytest.fixture
def mock_schedule_fail_teacher():
    schedule = Schedule(
        name="mock_schedule",
        n_days=1,
        n_periods=1,
        courses_size=2,
        rooms_size=2,
        curricula_size=2,
        constraints_size=0,
    )
    schedule.courses = [Course(
        id=f"course_{_}",
        teacher_id=f"teacher_0",
        n_students=10,
        n_lectures=1,
        min_working_days=1
    ) for _ in range(schedule.courses_size)]
    schedule.curricula = [Curriculum(
        id=f"curriculum_0",
        members=[schedule.courses[_].id]
    ) for _ in range(schedule.curricula_size)]
    return schedule

class TestConflictChecker:
    # TODO fix the score, because if course_0 and course_1 have a conflict, the score is 1, not 2
    def test_check_conflict_pass(self, mock_schedule_success: Schedule):
        """In a schedule with 2 courses, of different curricula, in different rooms, in the same period, there is no conflict"""
        matrix = [[0],
                  [1]]
        schedule = mock_schedule_success
        score = check_conflicts(matrix, schedule)
        assert score == 0

    def test_check_curricula_conflict_fail(self, mock_schedule_fail: Schedule):
        """In a schedule with 2 courses, of the same curricula, in different rooms, in the same period, there is a conflict"""
        matrix = [[0],
                  [1]]
        schedule = mock_schedule_fail
        score = check_conflicts(matrix, schedule)
        assert score == 2
    
    def test_check_teacher_conflict_fail(self, mock_schedule_fail_teacher: Schedule):
        """In a schedule with 2 courses, of the same curricula, in different rooms, in the same period, there is a conflict"""
        matrix = [[0],
                  [1]]
        schedule = mock_schedule_fail_teacher
        score = check_conflicts(matrix, schedule)
        assert score == 2
