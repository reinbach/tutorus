import logging

from django import template

log = logging.getLogger(__name__)
register = template.Library()

@register.inclusion_tag("questions/latest.html")
def latest_questions(classroom, user):
    question_list = classroom.latest_unanswered_questions(user)
    return {"questions": question_list}

@register.inclusion_tag("questions/answered.html")
def answered_questions(classroom):
    question_list = classroom.answered_questions()
    return {"questions": question_list}

@register.inclusion_tag("questions/top.html", takes_context=True)
def top_questions(context, classroom):
    user = context['user']
    question_list = classroom.top_questions()
    return {
        "questions": question_list,
        "is_tutor": classroom.is_tutor(user)
    }
