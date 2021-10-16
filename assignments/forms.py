from django.forms import ModelForm, inlineformset_factory

from assignments.models import QuestionSubmission, AssignmentSubmission


class QuestionSubmissionForm(ModelForm):
    class Meta:
        model = QuestionSubmission
        exclude = ()


QuestionSubmissionFormSet = inlineformset_factory(AssignmentSubmission, QuestionSubmission,
                                                  form=QuestionSubmissionForm, extra=0)
