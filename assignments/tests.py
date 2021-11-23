from django.test import TestCase
from django.urls import reverse

from .models import Assignment, Question
from courses.models import Course
from users.models import AppUser


class AssignmentModelTestCase(TestCase):
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
    def setUp(self):
        instructor = AppUser.objects.create(username="instructor1", is_instructor=True)
        instructor.set_password("password")
        instructor.save()
        student = AppUser.objects.create(username="student1")
        student.set_password("password")
        student.save()

        instructor2 = AppUser.objects.create(username="instructor2", is_instructor=True)
        instructor2.set_password("password")
        instructor2.save()

        course = Course.objects.create(name="CS 101", instructor=instructor)
        course.students.set((student,))

        self.assignment1 = Assignment.objects.create(name="Assignment 1", course=course)

        self.assignment2 = Assignment.objects.create(name="Assignment 2", course=course)
        self.question1 = Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=self.assignment2)
        self.question2 = Question.objects.create(index=2, question_body="Question 2", point_value=2, assignment=self.assignment2)
        self.question3 = Question.objects.create(index=3, question_body="Question 3", point_value=3, assignment=self.assignment2)
        self.assignment2.to_state_published()
        self.assignment2.save()

        self.assignment3 = Assignment.objects.create(name="Assignment 3", course=course)
        self.q1A3 = Question.objects.create(index=1, question_body="Q1A3", point_value=1, assignment=self.assignment3)
        self.q2A3 = Question.objects.create(index=2, question_body="Q2A3", point_value=2, assignment=self.assignment3)
        self.q3A3 = Question.objects.create(index=3, question_body="Q3A3", point_value=3, assignment=self.assignment3)
        self.assignment3.to_state_published()
        self.assignment3.save()

        self.assignment4 = Assignment.objects.create(name="Assignment 4", course=course)
        self.q1A4 = Question.objects.create(index=1, question_body="Q1A4", point_value=1, assignment=self.assignment4)
        self.q2A4 = Question.objects.create(index=2, question_body="Q2A4", point_value=2, assignment=self.assignment4)
        self.q3A4 = Question.objects.create(index=3, question_body="Q3A4", point_value=3, assignment=self.assignment4)
        self.assignment3.save()

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

    def test_student_unpublished_assignment_view(self):
        """
        Student can not see unpublished assignments
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment1.slug}))
        # response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment1.slug}))
        # self.assertEqual(response.status_code, 302)
        # response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment1.slug}), follow=True)
        # self.assertEqual(response.status_code, 200)

    def test_unauthorized_instructor_unpublished_assignment_view(self):
        """
        Instructor with no course can not see unpublished assignments
        """
        username = "instructor2"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment1.slug}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment1.slug}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_instructor_published_assignment_view(self):
        """
        Instructor with no course can not see published assignments
        """
        username = "instructor2"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment2.slug}))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment2.slug}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_instructor_published_assignment_view_multiple_questions(self):
        """
        Instructor can see questions in published assignment
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.q1A3.question_body)
        self.assertContains(response, self.q2A3.question_body)
        self.assertContains(response, self.q3A3.question_body)

    def test_instructor_unpublished_assignment_view_multiple_questions(self):
        """
        Instructor can see questions in unpublished assignment
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('assignments:view_assignment', kwargs={'slug': self.assignment4.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.q1A4.question_body)
        self.assertContains(response, self.q2A4.question_body)
        self.assertContains(response, self.q3A4.question_body)
