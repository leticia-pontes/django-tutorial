from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

# Função recebe requisição. Não importa requisição pois ainda não especificou a requisição.
def index(request: HttpRequest):
    print(request)
    print(request.headers)
    print(request.body)
    return HttpResponse(
        f"Hello, World! {request.headers['User-Agent']}",
        status=404,
    )