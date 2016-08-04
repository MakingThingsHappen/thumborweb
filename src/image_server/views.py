# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import json
from django.http import HttpResponse, Http404
from django.template import loader
from django.conf import settings
from django.shortcuts import render
from .utils import remove, generate_thumbor_cached_link
from .forms import FileNameForm
from .cloudflare import CloudFlare

cf = CloudFlare(settings.CLOUDFLARE_EMAIL,
                settings.CLOUDFLARE_API_KEY)


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
    files = os.listdir(settings.FILE_STORAGE_PATH)
    error = None
    if request.method == 'POST':
        form = FileNameForm(data=request.POST)
        if form.is_valid():
            image_url = form.cleaned_data['filename']
            # Removing thumbor file cached.
            try:
                remove(image_url)
            except OSError as e:
                raise Http404(str(e))
            msg = 'file:{} in thumbor removed successful.'.format(image_url)
            # Removing cloudflare file cached.
            cached_link = generate_thumbor_cached_link(
                            image_url, width=0, height=100, Smart=True)
            cached_link2 = generate_thumbor_cached_link(
                            image_url, width=0, height=140, Smart=True)
            resp = cf.purge_individual_files(settings.CLOUDFLARE_ZONE,
                                             [cached_link, cached_link2])
            content = json.loads(resp.content)
            is_success = content['success']
            if is_success:
                msg += '\nAnd cloudflare removed successful.'
            else:
                msg += '\nBut cloudflare remove failed.'

            return render(request,
                          'image_server/deleted.html',
                          {'removed_detail': msg})

            # return redirect(reverse_lazy('images:removed', kwargs={'filename': image_url}))
    template = loader.get_template(
        'image_server/form.html')

    return HttpResponse(template.render({'form': form,
                                         'files': files,
                                         'error': error},
                                        request))


def removed(request, filename):
    return render(request,
                  'image_server/deleted.html',
                  {'filename': filename})
