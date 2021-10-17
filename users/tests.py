from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from users.models import AppUser


class HomeViewTests(TestCase):
    def setUp(self):
        instructor1 = AppUser.objects.create(username="instructor1", is_instructor=True)
        instructor1.set_password("password")
        instructor1.save()
        student1 = AppUser.objects.create(username="student1")
        student1.set_password("password")
        student1.save()

        instructor2 = AppUser.objects.create(username="instructor2", is_instructor=True)
        instructor2.set_password("password")
        instructor2.save()
        student2 = AppUser.objects.create(username="student2")
        student2.set_password("password")
        student2.save()

        self.course1 = Course.objects.create(name="CS 101", instructor=instructor2)
        self.course1.students.add(student2)
        self.course1.save()

        self.course2 = Course.objects.create(name="CS 102", instructor=instructor2)
        self.course2.students.add(student2)
        self.course2.save()

        self.course3 = Course.objects.create(name="CS 103", instructor=instructor2)
        self.course3.students.add(student2)
        self.course3.save()

    def test_unauthenticated_homepage(self):
        """
        If user is not logged in show landing page
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to PeerGrader!")

    def test_student_homepage(self):
        """
        If authenticated user is student, show student homepage
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Welcome to PeerGrader!")
        self.assertContains(response, f"Hi {username}!")
        self.assertNotContains(response, "Instructor")

    def test_instructor_homepage(self):
        """
        If user is not logged in show landing page
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Welcome to PeerGrader!")
        self.assertContains(response, f"Hi Instructor {username}")

    def test_student_homepage_no_enrolled_courses(self):
        """
        If student is not enrolled in any courses, show a corresponding message
        """
        username = "student1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not currently enrolled in any classes.")
        self.assertQuerysetEqual(response.context['student_courses'], [])

    def test_instructor_homepage_no_taught_courses(self):
        """
        If instructor is not teaching in any courses, show a corresponding message
        """
        username = "instructor1"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not currently teaching any courses.")
        self.assertQuerysetEqual(response.context['instructor_courses'], [])

    def test_student_homepage_multiple_enrolled_courses(self):
        """
        If student is enrolled in courses, list them
        """
        username = "student2"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{self.course1.name} - {self.course1.instructor.username}")
        self.assertContains(response, f"{self.course2.name} - {self.course2.instructor.username}")
        self.assertContains(response, f"{self.course3.name} - {self.course3.instructor.username}")
        self.assertQuerysetEqual(response.context['student_courses'], [self.course1, self.course2, self.course3])

    def test_instructor_homepage_multiple_taught_courses(self):
        """
        If instructor is teaching courses, list them
        """
        username = "instructor2"
        password = "password"
        self.client.login(username=username, password=password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"{self.course1.name}")
        self.assertContains(response, f"{self.course2.name}")
        self.assertContains(response, f"{self.course3.name}")
        self.assertQuerysetEqual(response.context['instructor_courses'], [self.course1, self.course2, self.course3])