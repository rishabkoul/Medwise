from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from query.models import Query
from query.views import get_query_queryset
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from userprofile.models import UserProfile
from django.core.mail import EmailMessage
from django.views import View
from django.urls import reverse
from account.models import Account
from django.conf import settings
from django.contrib import messages

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from account.utils import token_generator

import threading

QUERIES_PER_PAGE = 25


class EmailThread(threading.Thread):

    def __init__(self, sendemail):
        self.sendemail = sendemail
        threading.Thread.__init__(self)

    def run(self):
        self.sendemail.send(fail_silently=False)


def index(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    return render(request, 'index.html', context=context)


def home(request):
    if not request.user.is_authenticated:
        return redirect("index")

    context = {}

    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    else:
        return redirect('userprofile:create')

    user_query = ""
    if request.GET:
        user_query = request.GET.get('q', '')
        context['user_query'] = str(user_query)

    queries = sorted(get_query_queryset(request=request, query=user_query),
                     key=attrgetter('date_updated'), reverse=True)

    page = request.GET.get('page', 1)
    query_paginator = Paginator(queries, QUERIES_PER_PAGE)

    try:
        queries = query_paginator.page(page)
    except PageNotAnInteger:
        queries = query_paginator.page(QUERIES_PER_PAGE)
    except EmptyPage:
        queries = query_paginator.page(query_paginator.num_pages)

    context['queries'] = queries

    return render(request, 'home.html', context=context)


def adviced(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.atype == 'Patient':
        return redirect("cantenter")

    context = {}

    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    else:
        return redirect('userprofile:create')

    user_query = ""
    if request.GET:
        user_query = request.GET.get('q', '')
        context['user_query'] = str(user_query)

    queries = sorted(get_query_queryset(request=request, query=user_query, advice=True),
                     key=attrgetter('date_updated'), reverse=True)

    page = request.GET.get('page', 1)
    query_paginator = Paginator(queries, QUERIES_PER_PAGE)

    try:
        queries = query_paginator.page(page)
    except PageNotAnInteger:
        queries = query_paginator.page(QUERIES_PER_PAGE)
    except EmptyPage:
        queries = query_paginator.page(query_paginator.num_pages)

    context['queries'] = queries

    return render(request, 'adviced.html', context=context)


def unadviced(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.atype == 'Patient':
        return redirect("cantenter")

    context = {}

    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    else:
        return redirect('userprofile:create')

    user_query = ""
    if request.GET:
        user_query = request.GET.get('q', '')
        context['user_query'] = str(user_query)

    queries = sorted(get_query_queryset(request=request, query=user_query, unadvice=True),
                     key=attrgetter('date_updated'), reverse=True)

    page = request.GET.get('page', 1)
    query_paginator = Paginator(queries, QUERIES_PER_PAGE)

    try:
        queries = query_paginator.page(page)
    except PageNotAnInteger:
        queries = query_paginator.page(QUERIES_PER_PAGE)
    except EmptyPage:
        queries = query_paginator.page(query_paginator.num_pages)

    context['queries'] = queries

    return render(request, 'unadviced.html', context=context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(form.cleaned_data)
            email = form.cleaned_data.get('email')
            atype = form.cleaned_data.get('atype')
            if atype != 'Doctor':
                user = Account.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                if settings.DEBUG:
                    activate_url = 'http://'+domain+link
                else:
                    activate_url = 'http://'+domain+link
                sendemail_body = 'Hi '+user.username + \
                    ' Please use this link to verify your account\n'+activate_url
                sendemail = EmailMessage(
                    'Activate yout account',
                    sendemail_body,
                    'admin@medwise.in',
                    [email],
                )
                EmailThread(sendemail).start()
                context['docregister'] = 'Check your mail to activate your account(may take some time to arrive)'
            else:
                context['docregister'] = 'We will send you an email when your account will get activated by admin'
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context=context)

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context=context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    else:
        return redirect('userprofile:create')

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = 'Updated'
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form

    return render(request, 'account/account.html', context=context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})


def cantenter_view(request):
    context = {}
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    else:
        return redirect('userprofile:create')
    return render(request, 'account/cantenter.html', context=context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.error(request, 'User already activated')
                return redirect('login')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated succesfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
