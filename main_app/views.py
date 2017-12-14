from django.views.generic import TemplateView
# Create your views here.
class Dashboard(TemplateView):
    template_name = 'home.html'
