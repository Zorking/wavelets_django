import logging

import os

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from core.forms import TransformForm
from core.models import Transform
from core.utils import wavelet_transform

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    if request.method == 'POST':
        id_in_db = wavelet_transform(request)
        return HttpResponse(reverse('results', kwargs={'pk': id_in_db}), status=200)

    return render(request, 'home.html')


def show_results(request, pk):
    return render(request, 'show_transform_resoults.html',
                  {'form': TransformForm(instance=Transform.objects.get(id=pk))})


