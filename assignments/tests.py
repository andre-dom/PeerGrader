from django.test import TestCase
from django.urls import reverse

from .models import Assignment, Question
from courses.models import Course
from users.models import AppUser


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


class AssignmentViewTestCase(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.Question = None

    def setUp(self):
        instructor = AppUser.objects.create(username="instructor1", is_instructor=True)
        instructor.set_password("password")
        instructor.save()
        student = AppUser.objects.create(username="student1")
        student.set_password("password")
        student.save()

        course = Course.objects.create(name="CS 101", instructor=instructor)
        course.students.set((student,))

        self.assignment1 = Assignment.objects.create(name="Assignment 1", course=course)

        self.assignment2 = Assignment.objects.create(name="Assignment 1", course=course)
        self.question1 = Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=self.assignment2)
        self.question2 = Question.objects.create(index=2, question_body="Question 2", point_value=2, assignment=self.assignment2)
        self.question3 = Question.objects.create(index=3, question_body="Question 3", point_value=3, assignment=self.assignment2)
        self.assignment2.to_state_published()
        self.assignment2.save()

    def test_instructor_unpublished_assignment_view_no_questions(self):
        """
        If there are no questions, show a corresponding message
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no questions.")

    def test_student_published_assignment_view_multiple_questions(self):
        """
        If there are questions show them
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment2.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question1.question_body)
        self.assertContains(response, self.question2.question_body)
        self.assertContains(response, self.question3.question_body)