from django.shortcuts import render, redirect, get_object_or_404
from query.models import Query
from comments.forms import CreateComment
from account.models import Account
from userprofile.models import UserProfile
from comments.models import Comment
from django.utils.text import slugify
from django.views.generic import View

# Create your views here.


def get_comments(query):
    comments = Comment.objects.filter(
        commented_on=query).order_by("-date_published")
    for comment in comments:
        comment.slug = slugify(
            comment.written_by.username+str(comment.written_by.pk))
    return comments


def create_comment_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    query = get_object_or_404(Query, slug=slug)

    if user.atype != 'Doctor':
        if user != query.patient:
            return redirect('cantenter')

    profile = UserProfile.objects.filter(user=request.user)
    if not profile:
        return redirect("userprofile:create")

    context['query'] = query

    form = CreateComment(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        writing_user = Account.objects.filter(email=user.email).first()
        obj.written_by = writing_user
        obj.commented_on = query
        obj.save()
        form = CreateComment()
        profile = profile.first()
        profile.comment_on.add(query)
        profile.save()
        if user.atype == 'Doctor':
            query.commented_by.add(user)
            query.save()
        return redirect("query:detail", slug=query.slug)

    return render(request, 'something_went_wrong.html', context=context)


class Delete_comment(View):

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            comment_id = kwargs['id']
            comment = Comment.objects.get(pk=comment_id)
            slugpass = comment.commented_on.slug
            comment.delete()
            query = Query.objects.filter(slug=slugpass).first()
            is_comment = Comment.objects.filter(
                written_by=request.user, commented_on=query)
            if not is_comment:
                query.commented_by.remove(request.user)
            return redirect('query:detail', slugpass)
