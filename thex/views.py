from django.http import HttpResponse
from django.shortcuts import render_to_response
from thex import models


def index(request):
    return HttpResponse("Hello, world. You're at the THEx index.")


def transients(request):
    return render_to_response('transients.html',
                              {'transients': models.Transient.objects.all()})