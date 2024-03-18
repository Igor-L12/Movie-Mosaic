from django.shortcuts import render

from django.http import HttpResponse

def about(request):
    template_name = 'catalog/about.html'
    return render(request, template_name)

def rules(request):
    template_name = 'catalog/rules.html'
    return render(request, template_name)

