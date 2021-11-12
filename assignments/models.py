import random

import pytz
from autoslug import AutoSlugField
from datetime import datetime, timedelta
from django_fsm import FSMField, transition

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import courses
import peerGrader

utc = pytz.UTC


class Assignment(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=utc.localize(datetime.now() + timedelta(days=1)),
                                    validators=[MinValueValidator(limit_value=utc.localize(datetime.now()))])
    course = models.ForeignKey('courses.Course', related_name='assignments', on_delete=models.CASCADE, )
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)
    state = FSMField(default="unpublished", protected=True)

    # publish assignment
    # preconditions:
    # assignment must have at least 1 question
    # class must have at least 1 student
    # postconditions:
    # assignment_submission and question_submission models will be created for every student in the class

    def can_publish(self):
        if self.numQuestions() > 0 and self.due_date > utc.localize(datetime.now()):
            return True
        return False

    @transition(field=state, source="unpublished", target="published", conditions=[can_publish])
    def to_state_published(self):
        # create assignment submissions for every student when assignment is published
        for student in self.course.students.all():
            assignment_submission = AssignmentSubmission.objects.create(student=student, assignment=self)
            for question in self.questions.all():
                QuestionSubmission.objects.create(AssignmentSubmission=assignment_submission, question=question)

    # unpublish assignment
    # postconditions:
    # all assignment_submission and question_submission models will be deleted

    def can_unpublish(self):
        return True

    @transition(field=state, source="published", target="unpublished", conditions=[can_unpublish])
    def to_state_unpublished(self):
        # delete all associated assignment submissions when assignment is unpublished
        self.assignment_submissions.all().delete()

    # close assignment submissions
    # preconditions:
    # current datetime must be after due date
    # postconditions:
    # will create and assign peer reviews to students.

    def can_close(self):
        if self.numQuestions() > 0 and self.due_date <= utc.localize(datetime.now()):
            return True
        return False

    @transition(field=state, source="published", target="closed", conditions=[can_close])
    def to_state_closed(self):
        assignedStudents = []  # make dictionary for multiple peer reviews
        for assignment_submission in self.assignment_submissions.filter(is_submitted=True):
            for i in range(0, 1):
                # get a student that has not yet been assigned a peer review
                students = self.course.students.all()
                student = random.choice(students)
                while student in assignedStudents or assignment_submission.student == student:
                    student = random.choice(students)
                assignedStudents.append((student, ))

                graded_assignment_submission = GradedAssignmentSubmission.objects.create(assignment_submission=assignment_submission, grader=student, assignment=self)
                for question_submission in assignment_submission.question_submissions.all():
                    GradedQuestionSubmission.objects.create(GradedAssignmentSubmission=graded_assignment_submission, QuestionSubmission=question_submission)

    def can_graded(self):
        return True

    @transition(field=state, source="closed", target="graded", conditions=[can_graded])
    def to_state_graded(self):
        pass

    def __str__(self):
        return self.name

    def numQuestions(self):
        return len(self.questions.all())

    def pointTotal(self):
        t = 0
        for q in self.questions.all():
            t += q.point_value
        return t


class Question(models.Model):
    question_body = models.TextField()
    point_value = models.IntegerField(validators=[MinValueValidator(0)])
    assignment = models.ForeignKey('Assignment', related_name='questions', on_delete=models.CASCADE, )
    index = models.IntegerField(validators=[MinValueValidator(1)])


class AssignmentSubmission(models.Model):
    student = models.ForeignKey(peerGrader.settings.AUTH_USER_MODEL,
                                related_name='submissions',
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_instructor': False}, )
    assignment = models.ForeignKey('Assignment', related_name='assignment_submissions', on_delete=models.CASCADE, )
    score = models.IntegerField(default=-1, )
    is_submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.assignment.course.name + ", " + self.assignment.name + ": " + self.student.username


class QuestionSubmission(models.Model):
    answer_body = models.TextField()
    AssignmentSubmission = models.ForeignKey('AssignmentSubmission', related_name='question_submissions',
                                             on_delete=models.CASCADE, )
    question = models.ForeignKey('Question', related_name='question_submissions', on_delete=models.CASCADE, )
    points = models.IntegerField(default=-1, )


class GradedAssignmentSubmission(models.Model):
    assignment_submission = models.ForeignKey('AssignmentSubmission', related_name='graded_assignment_submissions',
                                              on_delete=models.CASCADE, )
    assignment = models.ForeignKey('Assignment', related_name='graded_assignment_submissions', on_delete=models.CASCADE, default=None)
    grader = models.ForeignKey(peerGrader.settings.AUTH_USER_MODEL,
                               related_name='peer_reviews',
                               on_delete=models.CASCADE,
                               limit_choices_to={'is_instructor': False}, )
    is_submitted = models.BooleanField(default=False)


class GradedQuestionSubmission(models.Model):
    points = models.IntegerField(default=-1, )
    GradedAssignmentSubmission = models.ForeignKey('GradedAssignmentSubmission', related_name='graded_question_submissions',
                                                   on_delete=models.CASCADE, )
    QuestionSubmission = models.ForeignKey('QuestionSubmission', related_name='graded_question_submissions',
                                           on_delete=models.CASCADE, )

