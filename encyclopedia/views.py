from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django import forms
from . import util
from django.urls import reverse
from django.utils.safestring import mark_safe

class CreatePage(forms.Form):
    title = forms.CharField(label=mark_safe("Title"), widget=forms.TextInput(attrs={'size': '80', 'required': True}))
    forms.HiddenInput()
    page = forms.CharField(label=mark_safe("Body"), widget=forms.Textarea(attrs={'required': True}))
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


def index(request):
    print("index run")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "pageText": util.get_entry(title)
    })

def createPage(request):
    return render(request, "encyclopedia/create.html", {
        "form": CreatePage()
    })

def createAPI(request):
    if request.method == "POST":
        form = CreatePage(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["page"])
            return HttpResponseRedirect("/")
        else:
            return HttpResponseBadRequest("Bad form.")
    else:
        return HttpResponseBadRequest("Bad method.")