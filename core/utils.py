import json
import os
import io
import uuid

import numpy as np
import matplotlib.pyplot as plt
from django.core.files.base import ContentFile

from wavelets import WaveletAnalysis
from wavelets import Morlet, Paul, DOG, Ricker, Marr, Mexican_hat
from core.models import Transform


def wavelet_transform(request):
    time, low_resolution_signal, high_resolution_signal = get_data_from_file(request)
    x = np.array(high_resolution_signal)
    # and a sample spacing
    dt = 0.00025
    wavelets = {'1': Morlet(), '2': Paul(), '3': DOG(), '4': Ricker(), '5': Marr(), '6': Mexican_hat()}
    wa = WaveletAnalysis(x, wavelet=wavelets.get(request.POST.get('wavelet')), dt=dt)

    # wavelet power spectrum
    power = wa.wavelet_power

    # scales
    scales = wa.scales

    # associated time vector
    t = wa.time
    fig, ax = plt.subplots()
    T, S = np.meshgrid(t, scales)
    ax.contourf(T, S, power, 100)
    ax.set_yscale('log')
    f = io.BytesIO()
    fig.savefig(f, format="png")
    content_file = ContentFile(f.getvalue())
    transform = Transform(file_name=request.FILES['file'].name, channel=int(request.POST.get('channel')))
    transform.wavelet.save(str(uuid.uuid4()) + 'wavelet.png', content_file)
    plt.close()
    f.close()
    plt.plot(time, low_resolution_signal)
    plt.xlabel('Seconds')
    plt.ylabel('mV')
    f = io.BytesIO()
    plt.savefig(f, format='png')
    content_file = ContentFile(f.getvalue())
    transform.standart_cardio.save(str(uuid.uuid4()) + 'standart_cardio.png', content_file)
    plt.close()
    f.close()
    return transform.id


def get_data_from_file(request):
    channel_types_number = 2
    low_resolution_channel = 1 if request.POST.get('channel') == '1' else int(
        request.POST.get('channel')) + channel_types_number
    high_resolution_channel = low_resolution_channel + 1
    with open(os.path.join('/tmp', request.FILES['file'].name), 'wb+') as f:
        for chunk in request.FILES['file'].chunks():
            f.write(chunk)
    with open(f.name, 'r') as f:
        time, low_resolution_signal, high_resolution_signal = [], [], []
        for line in f:
            arr = []
            for value in line.strip().split('\t'):
                try:
                    value = float(value.strip('﻿'))
                    arr.append(value)
                except ValueError:
                    break
            if not len(arr) == 0:
                time.append(arr[0])
                low_resolution_signal.append(arr[low_resolution_channel])
                high_resolution_signal.append(arr[high_resolution_channel])
    return time, low_resolution_signal, high_resolution_signal
