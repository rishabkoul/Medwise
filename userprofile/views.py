from django.shortcuts import render, redirect, get_object_or_404
from userprofile.models import UserProfile
from userprofile.forms import CreateProfileForm, UpdateProfileForm
from account.models import Account

# Create your views here.


def create_profile_view(request):

    context = {}

    if not request.user.is_authenticated:
        return redirect('must_authenticate')

    profile = UserProfile.objects.filter(user=request.user)

    if(profile):
        return redirect('cantenter')

    form = CreateProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        user = Account.objects.filter(email=request.user.email).first()
        obj.user = user
        obj.save()
        form = CreateProfileForm()
        return redirect('home')

    context['form'] = form
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()

    return render(request, "userprofile/create_profile.html", context=context)


def edit_profile_view(request):

    context = {}

    if not request.user.is_authenticated:
        return redirect("must_authenticate")

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.POST:
        form = UpdateProfileForm(request.POST or None,
                                 request.FILES or None, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            profile = obj
    form = UpdateProfileForm(
        initial={
            'phone': profile.phone,
            'qualification': profile.qualification,
            'year_of_ex': profile.year_of_ex,
        }
    )
    context['form'] = form
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()
    return render(request, 'userprofile/edit_profile.html', context=context)


def detail_profile_view(request, slug):
    context = {}
    viewprofile = get_object_or_404(UserProfile, slug=slug)
    if viewprofile.user.atype != 'Doctor':
        if request.user != viewprofile.user:
            if request.user.atype == 'Patient':
                return redirect('cantenter')
    context['viewprofile'] = viewprofile
    profile = UserProfile.objects.filter(user=request.user)
    if profile:
        context['profile'] = profile.first()

    return render(request, 'userprofile/detail_profile.html', context=context)
