from django.test import TestCase
from django.urls import reverse

from assignments.models import Assignment, Question
from courses.models import Course
from users.models import AppUser


class CourseViewTests(TestCase):
    def setUp(self):
        instructor = AppUser.objects.create(username="instructor1", is_instructor=True)
        instructor.set_password("password")
        instructor.save()
        student = AppUser.objects.create(username="student1")
        student.set_password("password")
        student.save()

        self.course1 = Course.objects.create(name="CS 101", instructor=instructor)
        self.course1.students.add(student)
        self.course1.save()

        self.assignment1 = Assignment.objects.create(name="Assignment 1", course=self.course1)
        Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=self.assignment1)
        self.assignment1.to_state_published()
        self.assignment1.save()
        self.assignment2 = Assignment.objects.create(name="Assignment 2", course=self.course1)
        Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=self.assignment2)
        self.assignment2.to_state_published()
        self.assignment2.save()
        self.assignment3 = Assignment.objects.create(name="Assignment 3", course=self.course1)
        Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=self.assignment3)
        self.assignment3.to_state_published()
        self.assignment3.save()

        self.course2 = Course.objects.create(name="CS 102", instructor=instructor)
        self.course2.students.add(student)
        self.course2.save()

        self.course3 = Course.objects.create(name="CS 103", instructor=instructor)
        self.course3.students.add(student)
        self.course3.save()

        self.assignment4 = Assignment.objects.create(name="Assignment 4", course=self.course3)
        self.assignment5 = Assignment.objects.create(name="Assignment 5", course=self.course3)
        Question.objects.create(index=1, question_body="Question 1", point_value=1, assignment=self.assignment5)
        self.assignment5.to_state_published()
        self.assignment5.save()
        self.assignment6 = Assignment.objects.create(name="Assignment 6", course=self.course3)

    def test_student_course_view_no_assignments(self):
        """
        If there are no assignments, show a corresponding message
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course2.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no assignments.")
        self.assertQuerysetEqual(response.context['assignments'], [])

    def test_student_course_view_multiple_assignments(self):
        """
        If there are assignments, show them
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{self.assignment1.name}")
        self.assertContains(response, f"{self.assignment2.name}")
        self.assertContains(response, f"{self.assignment3.name}")
        self.assertQuerysetEqual(response.context['assignments'],
                                 [self.assignment1, self.assignment2, self.assignment3])

    def test_student_course_view_unpublished_assignments(self):
        """
        If there are unpublished assignments, dont show them
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f"{self.assignment4.name}")
        self.assertContains(response, f"{self.assignment5.name}")
        self.assertNotContains(response, f"{self.assignment6.name}")
        self.assertQuerysetEqual(response.context['assignments'], [self.assignment5, ])

    def test_unenrolled_student_course_view(self):
        """
        If a student is not enrolled in a course, dont show them the course page
        """
        username = "student2"
        password = "password"
        student = AppUser.objects.create(username=username)
        student.set_password(password)
        student.save()

        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course1.slug}))
        self.assertEqual(response.status_code, 302) # Redirect home
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course1.slug}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f"{self.assignment1.name}")
        self.assertNotContains(response, f"{self.assignment2.name}")
        self.assertNotContains(response, f"{self.assignment3.name}")
        assert('assignments' not in response.context.keys())

    def test_instructor_course_view_no_assignments(self):
        """
        If there are no assignments, show a corresponding message
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course2.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no assignments.")
        self.assertQuerysetEqual(response.context['assignments'], [])

    def test_instructor_course_view_multiple_assignments(self):
        """
        If there are assignments, show them
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{self.assignment1.name}")
        self.assertContains(response, f"{self.assignment2.name}")
        self.assertContains(response, f"{self.assignment3.name}")
        self.assertQuerysetEqual(response.context['assignments'],
                                 [self.assignment1, self.assignment2, self.assignment3])

    def test_instructor_course_view_unpublished_assignments(self):
        """
        Instructors should see all assignments, even unpublished ones
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course3.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{self.assignment4.name}")
        self.assertContains(response, f"{self.assignment5.name}")
        self.assertContains(response, f"{self.assignment6.name}")
        self.assertQuerysetEqual(response.context['assignments'], [self.assignment4, self.assignment5, self.assignment6, ])

    def test_unauthorized_instructor_course_view(self):
        """
        If a student is not enrolled in a course, dont show them the course page
        """
        username = "instructor2"
        password = "password"
        instructor = AppUser.objects.create(username=username)
        instructor.set_password(password)
        instructor.save()

        self.client.login(username=username, password=password)
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course1.slug}))
        self.assertEqual(response.status_code, 302) # Redirect home
        response = self.client.get(reverse('courses:view_course', kwargs={'slug': self.course1.slug}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f"{self.assignment1.name}")
        self.assertNotContains(response, f"{self.assignment2.name}")
        self.assertNotContains(response, f"{self.assignment3.name}")
        assert('assignments' not in response.context.keys())
