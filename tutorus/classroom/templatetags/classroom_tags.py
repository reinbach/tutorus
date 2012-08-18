from django import template

register = template.Library()


@register.inclusion_tag("questions/latest.html")
def latest_questions(classroom, user):
    question_list = classroom.latest_unanswered_questions(user)
    return {"questions": question_list}


@register.inclusion_tag("questions/top.html")
def top_questions(classroom):
    question_list = classroom.top_questions()
    return {"questions": question_list}
