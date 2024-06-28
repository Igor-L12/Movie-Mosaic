from django.shortcuts import render

from django.views.generic import TemplateView

from cinema.models import VideoProduct, Actor, Director

from games.models import GameProduct

from serials.models import SerialProduct

from .forms import SearchForm

def search(request):
    query = request.GET.get('query')
    template_name = 'catalog/search_results.html'
    video_results = []
    game_results = []
    serial_results = []

    if query:
        video_results = VideoProduct.objects.filter(original_title__title__icontains=query)
        game_results = GameProduct.objects.filter(title__icontains=query)
        serial_results = SerialProduct.objects.filter(original_title__title__icontains=query)

    context = {
        'query': query,
        'video_results': video_results,
        'game_results': game_results,
        'serial_results': serial_results,
        'form': SearchForm()
    }

    return render(request, template_name, context)

class About(TemplateView):
    template_name = 'catalog/about.html'

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь ключ total_count;
        context.update({
            'total_count': VideoProduct.objects.count(),
            'actors_count': Actor.objects.count(),
            'directors_count': Director.objects.count(),
        })
        return context

class Rules(TemplateView):
    template_name = 'catalog/rules.html'


