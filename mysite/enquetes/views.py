from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Pergunta, escolha
from django.urls import reverse
from django.db.models import F

def index(request):
    ultimas_perguntas = Pergunta.objects.order_by('-data_publicacao')[:5]
    contexto = { 'ultimas_perguntas': ultimas_perguntas }
    return render(request, 'enquetes/index.html',contexto)

def detalhes(request, pergunta_id):
    try:
        pergunta = Pergunta.objects.get(pk=pergunta_id)
    except:
        raise Http404("A pergunta nao existe!")
    return render(request, 'enquetes/detalhes.html',{'pergunta':pergunta})

def resultados(request,pergunta_id):
    Pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    return render(request, "enquetes/resultados.html", {"pergunta": Pergunta})

def votos(request,pergunta_id):
    Pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        escolha_selecionada = Pergunta.escolha_set.get(pk=request.POST["escolha"])
    except (KeyError, escolha.DoesNotExist):
        return render(
            request,
            "enquetes/detalhes.html",
            {
                "question": Pergunta,
                "error_mensage": "vocé nao selecionou uma escolha."
            }
        )
    else:
        escolha_selecionada.votos = f("votos") + 1
        escolha_selecionada.save()


        return HttpResponseRedirect(reverse("enquetes:resultados", args=(pergunta_id,)))