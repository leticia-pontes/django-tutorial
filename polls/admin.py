from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline): # StackedInline: mostra as opções separadas; TabularInline: mostra as opções juntas
    model = Choice
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = [ # colunas mostradas na lista de questões
        "question_text", 
        "pub_date", 
        "was_published_recently"
    ]
    list_filter = ["pub_date"] # permite a filtragem por data
    search_fields = ["question_text", "choice__choice_text"] # busca por texto; __ entra em outra tabela

# admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)