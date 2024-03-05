from django.http import HttpResponseRedirect
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects \
            .filter(pub_date__lte=timezone.now()) \
            .order_by("-pub_date")[:5]

# Função recebe requisição. Não importa requisição pois ainda não especificou a requisição.
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# Cria uma view
# def create_detail_view(model):
#     class DetailViewNova(generic.DetailView):
#         model = model
#         template_name = "polls/results.html"
    
#     type('DetailViewNova', (generic(DetailView,)), {
#         'model': model,
#         'template_name': 
#     }),

#     return DetailViewNova

# DetailView = create_detail_view(Question)

def vote(request, question_id): # View Voto
    question = get_object_or_404(Question, pk=question_id) # Pega o objeto ou o erro
    try:
        # Objeto carregado do banco
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) # Pega as opções da Question específica
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render( #
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            }, # Retorna a questão e a mensagem de erro.
        )
    else:
        # Evita conflito de concorrência. 
        # Caso: duas pessoas votaram (passa de 1 para 3, por exemplo). Enquanto isso, outra pessoa vota e o valor dos votos não altera (vai de 2 para 3, por exemplo).
        selected_choice.votes = F("votes") + 1 # Incrementa os votos
        selected_choice.save() # Salva o voto

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) # Redireciona para a tela de Resultados
        # Se não utilizar o Redirect, a requisição POST continua armazenada
        # Reverse: retorna uma URL (relativa a uma View)
