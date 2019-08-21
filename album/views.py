from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime

import os

from .models import *


def error_404(request, exception):
    context = {"title": "Not found"}
    return render(request,'album/404.html', context)

def homepage(request):

    photos = Photo.objects.all().order_by('?')[:3]
    context = {
        "photos": photos
    }
    return render(request, 'album/index.html', context)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ["title", 'description', "category", "img"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Picture"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user.photographer
        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy("album:detail_photo", kwargs={
            'pk':self.object.pk,
            'slug':self.object.slug,
            'author_slug':self.request.user.photographer.slug
            })


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #attention, l'ordre des class importe!!!!
    model = Photo
    fields = ["title", 'description', "category"]
    template_name = "album/photo_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user.photographer
        return super().form_valid(form)

    def test_func(self):
        photo = self.get_object()
        if self.request.user.photographer == photo.author:
            return True
        else:
            return False

    def get_success_url(self):
        photo = self.get_object()
        return reverse_lazy("album:detail_photo", kwargs={
            'pk':photo.pk,
            'slug':photo.slug,
            'author_slug':photo.author.slug,
            })


class PhotoDetailView(DetailView):
    model = Photo
    context_object_name = "photo_info"
    template_name = "album/photo_detail.html"

    def get_context_data(self, **kwargs):

        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        comments = Paginator(self.object.comment_set.all().order_by("-date_posted"), 5)
        context['comments'] = comments.get_page(page)
        context['comments_number'] = self.object.comment_set.count()

        #check if picture file exists
        if os.path.isfile("."+self.object.img.url):
            context['allowed'] = True
        else:
            context['allowed'] = False


        # for the page title
        photo = self.get_object()
        context['title'] = photo.title

        return context


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    # gen template name = photo_confirm_delete

    def test_func(self):
        photo = self.get_object()
        if self.request.user.photographer == photo.author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse_lazy("photographer_home", kwargs={'slug':self.request.user.photographer.slug,})


def search_bar_view(request):
    context = {}
    context['photos'] = ""
    queryset = []

    if request.GET:
        query = request.GET['q']
        context['query'] = str(query) # pour l'expo dans le template

        queries = query.split(" ")
        for q in queries:
            photos = Photo.objects.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__icontains=q)
            ).distinct()

            for photo in photos:
                queryset.append(photo)

        context['photos'] = queryset
        context['title'] = str(query)

    return render(request, "album/search_results.html", context)



def AddCommentView(request):
    print("ajax departure")
    if request.method == 'POST':

        response_data = {}
        response_data['permission'] = False

        try:
            if request.POST.get("photoId"):
                clean_img_id = int(request.POST.get("photoId"))
                photo_id = request.POST.get("photoId")
            else:
                return JsonResponse(response_data)
        except ValueError:
            return JsonResponse(response_data)

        try:
            commented_photo = Photo.objects.get(pk=photo_id)
            content_text = request.POST.get('content')
            comment = Comment(content=content_text, author=request.user.photographer, article=commented_photo)
            comment.save()

            response_data['permission'] = True
            response_data['report'] = "{} has commented: {}".format(request.user.photographer.pk, content_text)
            response_data['userImg'] = str(request.user.photographer.image)
            response_data['username'] = str(request.user.username)
            response_data['newCommentId'] = comment.pk

            date_cur = datetime.now()
            response_data['date'] = date_cur.strftime("%m/%d, %H:%M")

            return JsonResponse(response_data)
        except Photo.DoesNotExist:
            return JsonResponse(response_data)

    else:
        return HttpResponse(
            "error"
        )


def DeleteCommentView(request):

    response_data = {}
    response_data["permission"] = False

    if request.POST.get("targetCommentId") and request.POST.get("photoId"):

        try:
            cleaned_commentId = int(request.POST.get("targetCommentId"))
            cleaned_photoId = int(request.POST.get("photoId"))
        except ValueError:
            return JsonResponse(response_data)

        try:
            photo = Photo.objects.get(pk=cleaned_photoId)
            comment = Comment.objects.get(pk=cleaned_commentId)
            photographer = request.user.photographer

            if comment.article != photo or (comment.author != photographer and photo.author != photographer):
                return JsonResponse(response_data)

            else:
                response_data["permission"] = True
                comment.delete()
                return JsonResponse(response_data)

        except Photo.DoesNotExist:
            return JsonResponse(response_data)

        except Comment.DoesNotExist:
            return JsonResponse(response_data)

    else:
        return JsonResponse(response_data)
