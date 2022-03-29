from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from .models import Posts
from fdap.definitions import LOG_PATH
from fdap.utils.util import config_json, write_config_json
from fdap.config.config import Config
from .forms import get_form
import os


# Create your views here.
def index(request):
    post_list = Posts.objects.all()
    return render(request, 'home.html', {'post_list': post_list})


def posts(request):
    post_list = Posts.objects.all()
    return render(request, 'posts.html', {'post_list': post_list})


def logs(request):
    log_list = os.listdir(LOG_PATH)

    logs_list = []
    recent = {}
    for con in log_list:
        if 'log' in con:
            try:
                name, ext, date = con.split('.')
                logs_list.append({'date': date, 'subject': con})
            except ValueError as e:
                name, ext = con.split('.')
                date = timezone.now().strftime('%Y-%m-%d')
                recent = {'date': date, 'subject': con}

    logs_list.reverse()
    logs_list.insert(0, recent)

    return render(request, 'log_list.html', {'log_list': logs_list})


def log(request, f_name):
    f = open(LOG_PATH + '/' + f_name, 'r', encoding='utf-8')
    contents = f.read()

    return render(request, 'log.html', {'f_name': f_name, 'contents': contents})


def config(request, module):
    config_list = Config.list()

    conf = None
    if module in config_list:
        conf = config_json(module)

    return render(request, 'config_form.html', {'config': conf, 'module': module})


def write_config(request, module):
    if module in Config.list():
        data = get_form(module, request.POST)
        conf = write_config_json(module, data.to_dict())

    return redirect('config', module=module)
