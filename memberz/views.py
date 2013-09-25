from django.shortcuts import render_to_response
from models import *
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.xheaders import populate_xheaders
from django.core.paginator import Paginator, InvalidPage,EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.db.models import Q
from random import randint
#from pure_pagination.paginator import Paginator


