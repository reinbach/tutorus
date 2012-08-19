import json
import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

from classroom.models import ClassRoom

from core.utils import publish
from forms import AskQuestionForm, AnswerQuestionForm
from models import Question, QuestionVotes

log = logging.getLogger(__name__)

def valid_classroom(func):
    def decorator(request, classroom_id):
        if ClassRoom.objects.filter(pk=classroom_id).exists():
            classroom = ClassRoom.objects.get(pk=classroom_id)
            return func(request, classroom)
        return HttpResponseNotFound("Invalid Classroom")
    return decorator

def tutor_only(func):
    def decorator(request, question_id):
        question = Question.objects.get(pk=question_id)
        if question.classroom.is_tutor(request.user):
            return func(request, question)
        return HttpResponseBadRequest("Not the Tutor")
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
            channel = "classroom_{0}".format(classroom.pk)
            pub_message = {
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
            publish(channel, pub_message)
        else:
            message = {"error": form.errors}
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
        publish_top_questions(question.classroom)
        return HttpResponse(json.dumps({"success": question.pk}))
    return HttpResponseNotFound("Invalid question")

@login_required
@tutor_only
def answer_question(request, question):
    """Record answer to question, only tutors can answer question

    Then publish the event
    """
    if request.method == 'POST':
        form = AnswerQuestionForm(data=request.POST)
        message = {"success": True}
        if form.is_valid():
            question = form.save(question)
            channel = "classroom_{0}".format(question.classroom.pk)
            message = {
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
            publish(channel, message)
        else:
            message = {"error": form.errors}
            return HttpResponseBadRequest(message)
        return HttpResponse(json.dumps(message))
    return HttpResponseNotFound("Need to post")

def publish_top_questions(classroom):
    """Get a list of the highest voted questions for a classroom and publish"""
    top_questions = []
    for question in classroom.top_questions():
        top_questions.append({
            "pk": question.pk,
            "subject": question.subject,
            "content": question.content,
            "student": question.student.username,
            "vote_count": question.vote_count(),
        })
    channel = "classroom_{0}".format(classroom.pk)
    message = {
        "type": "top_question",
        "questions": top_questions
    }
    publish(channel, message)
