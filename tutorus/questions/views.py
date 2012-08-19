import json
import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

from classroom.models import ClassRoom

from core.utils import get_pubnub_connection
from forms import AskQuestionForm
from models import Question, QuestionVotes

log = logging.getLogger(__name__)

def valid_classroom(func):
    def decorator(request, classroom_id):
        if ClassRoom.objects.filter(pk=classroom_id).exists():
            classroom = ClassRoom.objects.get(pk=classroom_id)
            return func(request, classroom)
        return HttpResponseNotFound("Invalid Classroom")
    return decorator

@login_required
@valid_classroom
def ask_question(request, classroom):
    """Ask question for specific class

    Need to publish the question to rest of classroom
    """
    if request.method == 'POST':
        form = AskQuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(request.user, classroom)
            message = {"success": True}
            pubnub = get_pubnub_connection()
            pubnub.publish({
                "channel": "classroom_{0}".format(classroom.pk),
                "message": {
                    "type": "new_question",
                    "question": {
                        "pk": question.pk,
                        "subject": question.subject,
                        "content": question.content,
                        "student": question.student.username,
                        "up_vote_url": reverse(
                            "question_up_vote", args=[question.pk]
                        ),
                    }
                }
            })
        else:
            message = {"error": form.errors}
            print message
            return HttpResponseBadRequest(message)
        return HttpResponse(json.dumps(message))
    return HttpResponseNotFound("Need to post")

@login_required
def up_vote_question(request, question_id):
    """Up vote specific question

    Can only be done once by the student
    """
    if Question.objects.filter(pk=question_id).exists():
        question = Question.objects.get(pk=question_id)
        # ensure student has not voted before for this question
        if QuestionVotes.objects.filter(
            question=question,
            voter=request.user
        ).exists():
            return HttpResponseNotFound("Already voted")
        vote = QuestionVotes.objects.create(
            question=question,
            voter=request.user
        )
        vote.save()
        return HttpResponse(json.dumps({"success": question.pk}))
    return HttpResponseNotFound("Invalid question")

def publish_top_questions(classroom):
    """Get a list of the highest voted questions for a classroom and publish"""
    pass