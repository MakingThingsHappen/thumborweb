# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed

REPO = ''
