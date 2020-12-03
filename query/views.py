from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from query.models import Query
from query.forms import CreateQueryForm, UpdateQueryForm
from account.models import Account
from userprofile.models import UserProfile
from comments.views import get_comments
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import View

# Create your views here.
COMMENTS_PER_PAGE = 25


def create_query_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    if user.atype == 'Doctor':
        return redirect('query:docs_not_allowed')

    form = CreateQueryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        patient = Account.objects.filter(email=user.email).first()
        obj.patient = patient
        obj.save()
        form = CreateQueryForm()
        return redirect('home')

    context['form'] = form
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()

    return render(request, "query/create_query.html", context=context)


def docs_not_allowed_view(request):
    context = {}
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    return render(request, 'query/docs_not_allowed.html', context=context)


def detail_query_view(request, slug):
    context = {}
    query = get_object_or_404(Query, slug=slug)
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    if request.user != query.patient:
        if request.user.atype == 'Patient':
            return redirect('cantenter')
    context['query'] = query
    profile = UserProfile.objects.filter(user=request.user)
    seeing_profile = UserProfile.objects.filter(user=query.patient)
    if seeing_profile:
        context['seeing_profile'] = seeing_profile.first()
    if profile:
        context['profile'] = profile.first()

    queries = get_comments(query)

    page = request.GET.get('page', 1)
    query_paginator = Paginator(queries, COMMENTS_PER_PAGE)

    try:
        queries = query_paginator.page(page)
    except PageNotAnInteger:
        queries = query_paginator.page(COMMENTS_PER_PAGE)
    except EmptyPage:
        queries = query_paginator.page(query_paginator.num_pages)

    context['queries'] = queries

    return render(request, 'query/detail_query.html', context=context)


def edit_query_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    query = get_object_or_404(Query, slug=slug)
    if user != query.patient:
        return redirect("cantenter")

    if request.POST:
        form = UpdateQueryForm(request.POST or None,
                               request.FILES or None, instance=query)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.POST.get('clear_image_image'):
                obj.image = None
            if request.POST.get('clear_image_image2'):
                obj.image2 = None
            if request.POST.get('clear_image_image3'):
                obj.image3 = None
            if request.POST.get('clear_image_image4'):
                obj.image4 = None
            if request.POST.get('clear_image_image5'):
                obj.image5 = None
            if request.POST.get('clear_image_image6'):
                obj.image6 = None
            if request.POST.get('clear_image_image7'):
                obj.image7 = None
            if request.POST.get('clear_image_image8'):
                obj.image8 = None
            if request.POST.get('clear_image_image9'):
                obj.image9 = None
            if request.POST.get('clear_image_image10'):
                obj.image10 = None
            obj.save()
            context['success_message'] = 'Updated'
            query = obj
        else:
            errors = []
            for field in form:
                for error in field.errors:
                    errors.append(error)
            context['errors'] = errors
    form = UpdateQueryForm(
        initial={
            'heading': query.heading,
            'body': query.body,
            'image': query.image or None,
            'image2': query.image2 or None,
            'image3': query.image3 or None,
            'image4': query.image4 or None,
            'image5': query.image5 or None,
            'image6': query.image6 or None,
            'image7': query.image7 or None,
            'image8': query.image8 or None,
            'image9': query.image9 or None,
            'image10': query.image10 or None,
        }
    )
    context['form'] = form
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    return render(request, 'query/edit_query.html', context=context)


def get_query_queryset(request, query=None, advice=False, unadvice=False):
    aqset = []
    unqset = []
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        profile = profile.first()
    if query == "":
        if(request.user.atype == 'Doctor'):
            if advice == True:
                aqs = Query.objects.all()
                for aq in aqs:
                    if aq in profile.comment_on.all():
                        aqset.append(aq)
                return list(set(aqset))
            if unadvice == True:
                unqset = Query.objects.filter(commented_by=None)
                return list(set(unqset))
            return(Query.objects.all())
        else:
            return(Query.objects.filter(patient=request.user))

    queryset = []
    queries = query.split(" ")

    if(request.user.atype == 'Doctor'):
        if advice == True:
            for q in queries:
                posts = Query.objects.filter(
                    Q(heading__icontains=q) |
                    Q(body__icontains=q) |
                    Q(patient__username__icontains=q)
                ).distinct()

            for post in posts:
                if post in profile.comment_on.all():
                    queryset.append(post)
        elif unadvice == True:
            for q in queries:
                posts = Query.objects.filter(
                    Q(heading__icontains=q) |
                    Q(body__icontains=q) |
                    Q(patient__username__icontains=q)
                ).distinct()

            for post in posts:
                if post.commented_by == None:
                    queryset.append(post)

        else:
            for q in queries:
                posts = Query.objects.filter(
                    Q(heading__icontains=q) |
                    Q(body__icontains=q) |
                    Q(patient__username__icontains=q)
                ).distinct()

            for post in posts:
                queryset.append(post)
    else:
        for q in queries:
            posts = Query.objects.filter(
                Q(heading__icontains=q) | Q(body__icontains=q)).distinct()

        for post in posts:
            if post.patient == request.user:
                queryset.append(post)

    return list(set(queryset))


class Delete_query(View):

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            query_ids = request.POST.getlist('id[]')
            for id in query_ids:
                query = Query.objects.get(pk=id)
                query.delete()
            return redirect('home')
