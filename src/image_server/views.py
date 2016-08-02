# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from .forms import FileNameForm


def list_cwd_file(request):
    names = os.listdir(settings.PROJ_DIR)
    return render(request, 'image_server/list.html', {'names': names})


def remove_specify_file(request):
    """

    Args:
        request:

    Returns:

    """
    form = FileNameForm()
    files = os.listdir(settings.TEST_PATH)
    error = None
    if request.method == 'POST':
        form = FileNameForm(data=request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            path = os.path.join(settings.TEST_PATH, filename)
            has_file = os.path.exists(path)
            if has_file:
                os.remove(path)
                return redirect(reverse_lazy('images:removed', kwargs={'filename': filename}))
            else:
                error = 'The file:"{}" is not found'.format(filename)
    template = loader.get_template(
        'image_server/form.html'
    )

    return HttpResponse(template.render({'form': form,
                                         'files': files,
                                         'error': error},
                                        request))


def removed(request, filename):
    return render(request,
                  'image_server/deleted.html',
                  {'filename': filename})
