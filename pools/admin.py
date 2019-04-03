from django.contrib import admin

# Register your models here.
from .models import Question, Choice

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [(None, {'fields': ['question_text']}), ('Date infomation', {'fields':['pub_data']}), ]
#     #fields=['pub_data', 'question_text']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['question_text']}), ('Date information', {'fields': ['pub_data'], 'classes':['collapse']}),]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_data', 'was_published_recently')
    list_filter = ['pub_data']
    search_fields = ['question_text']
admin.site.register(Question, QuestionAdmin)
#admin.site.register(Question, QuestionAdmin)