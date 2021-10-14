from django.contrib import admin
from api.models import Answer, Choice, Form, Question, Submission

admin.site.register(Answer)
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Choice)
