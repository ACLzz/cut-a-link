import requests
import json
from os import environ
from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from cutter.forms import IndexForm

from string import ascii_letters
from random import choice

from .models import Link, Stats

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
shorty_length = 5


class IndexView(FormView):
    template_name = 'cutter/index.html'

    form_class = IndexForm
    success_url = '/'

    def form_valid(self, form):
        short = self.create_link(form.cleaned_data)
        self.form_class.short = short
        return self.get(self.request)

    def form_invalid(self, form):
        error = 'Error'
        self.form_class.error = error
        return self.get(self.request)

    def create_link(self, data):
        extra = False
        if data['type'] == 'Extra':
            extra = True

        orig = data['origin']
        short = generate_shorty(shorty_length)

        # If that url already exist in database
        exist = Link.objects.filter(orig=orig, extra=extra)
        if exist:
            return exist[0].short

        link = Link(orig=orig, short=short, extra=extra)
        link.save()
        return short


def extra(request, short):
    queryset = []
    for stat in Stats.objects.filter(short=short).order_by('-date'):
        stat.date = stat.date.strftime("%m/%d/%Y, %H:%M:%S")
        queryset.append(stat)

    context = {'redirections': queryset}
    return render(request, 'cutter/extra.html', context=context)


class ExtraView(DetailView):
    model = Stats
    template_name = 'cutter/extra.html'
    context_object_name = 'redirections'


def app_redirect(request, short):
    link = get_object_or_404(Link, short=short)

    if link.extra:
        key = environ.get("IP_API_KEY")
        ip = get_client_ip(request)
        ips = requests.get(f'http://api.ipstack.com/{ip}?access_key={key}')
        resp = json.loads(ips.text)

        if resp['ip'] == '127.0.0.1':
            return redirect(link.orig)

        agent = request.META['HTTP_USER_AGENT']
        long = resp['longitude']
        lat = resp['latitude']
        now = datetime.now()

        link.stats_set.create(
            ip=ip,
            date=now,
            long=long,
            lat=lat,
            agent=agent
        )

    return redirect(link.orig)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def generate_shorty(length):
    all_chars = []
    all_chars.extend(numbers)
    all_chars.extend(ascii_letters)

    return ''.join(str(choice(all_chars)) for _ in range(length))
