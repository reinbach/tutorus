import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound

from classroom.models import ClassRoom

from forms import AskQuestionForm
from core.utils import get_pubnub_connection

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
                        "subject": question.subject,
                        'content': question.content,
                        'student': question.student.username
                    }
                }
            })
        else:
            message = {"error": form.errors}
        return HttpResponse(json.dumps(message))
    return HttpResponseNotFound("Need to post")
