from django.test import TestCase
from .models import Assignment, Question
from courses.models import Course
from users.models import AppUser


# Create your tests here.
class AssignmentTestCase(TestCase):
    def setUp(self):
        instructor = AppUser.objects.create(username="instructor1", password="password", is_instructor=True)
        student = AppUser.objects.create(username="student1", password="password")
        course = Course.objects.create(name="CS 101", instructor=instructor)
        course.students.set((student,))
        assignment = Assignment.objects.create(name="Assignment 1", course=course)
        Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=assignment)
        Question.objects.create(index=2, question_body="Question 2", point_value=2, assignment=assignment)
        Question.objects.create(index=3, question_body="Question 3", point_value=3, assignment=assignment)

    def test_num_questions_func(self):
        """Test numQuestions returns the number of questions in the assignment"""
        assignment = Assignment.objects.get(name="Assignment 1")
        self.assertEqual(assignment.numQuestions(), 3)

    def test_point_total_func(self):
        """Test pointTotal returns the number of questions in the assignment"""
        assignment = Assignment.objects.get(name="Assignment 1")
        self.assertEqual(assignment.pointTotal(), 6)
