from django.test import TestCase
from django.urls import reverse

from assignments.models import Question, Assignment
from courses.models import Course
from users.models import AppUser



# class CourseViewTests(TestCase):
#
#     # def setUp(self):
#     #     instructor = AppUser.objects.create(username="instructor1", password="password", is_instructor=True)
#     #     student = AppUser.objects.create(username="student1", password="password")
#     #     course1 = Course.objects.create(name="CS 101", instructor=instructor, slug="cs-101")
#     #     course2 = Course.objects.create(name="CS 102", instructor=instructor, slug="cs-102")
#     #     course1.students.set((student,))
#     #     course2.students.set((student,))
#     #     assignment = Assignment.objects.create(name="Assignment 1", course=course1)
#
#     def test_student_course_view_no_courses(self):
#         """
#         If viewed course has no assignments a message is displayed
#         """
#         instructor = AppUser.objects.create(username="instructor1", password="password", is_instructor=True)
#         student = AppUser.objects.create(username="student1", password="password")
#         course = Course.objects.create(name="CS 101", instructor=instructor)
#         course.students.add(student)
#         response = self.client.post('/users/login/', {'username': 'student1', 'password': 'password'})
#         print(course.instructor.username)
#         response = self.client.get(reverse('view_course', course.slug))
#         self.assertEqual(response.status_code, 200)