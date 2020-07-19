from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django import forms
from . import util
from django.urls import reverse
from django.utils.safestring import mark_safe
import pprint
import random

class CreatePage(forms.Form):
    title = forms.CharField(label=mark_safe("Title"), widget=forms.TextInput(attrs={'size': '80', 'required': True}))
    page = forms.CharField(label=mark_safe("Body"), widget=forms.Textarea(attrs={'required': True}))

class EditPage(forms.Form):
    title = forms.CharField(label=mark_safe("Title"), widget=forms.TextInput(attrs={'size': '80', 'required': True}))
    page = forms.CharField(label=mark_safe("Body"), widget=forms.Textarea(attrs={'required': True}))

    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    if util.get_entry(title) == None:
        return HttpResponseBadRequest("Page does not exist.")
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "pageText": util.get_entry_html(title)
        })

def createPage(request):
    return render(request, "encyclopedia/create.html", {
        "form": CreatePage()
    })

def createAPI(request):
    if request.method == "POST":
        form = CreatePage(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data["title"]) != None:
                return HttpResponseBadRequest("Page already exist.")
            else:
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["page"])
                return HttpResponseRedirect("/"+form.cleaned_data["title"])
        else:
            return HttpResponseBadRequest("Bad form.")
    else:
        return HttpResponseBadRequest("Bad method.")

def searchPage(request, keyword):
    entries = util.list_entries()
    for entry in entries:
        if(entry.lower() == keyword.lower()):
            return HttpResponseRedirect("/"+keyword)

    searchResults = []
    # Deepsearch
    for entry in entries:
        page = util.get_entry(entry)
        if keyword.lower() in entry.lower() or keyword.lower() in page.lower():
            searchResults.append(entry)

    return render(request, "encyclopedia/searchResults.html", {
        "searchResults": searchResults,
        "searchResultsLength": len(searchResults)
    })

def editPage(request, title):
    return render(request, "encyclopedia/edit.html", {
        "form": EditPage(initial={"title": title, "page": util.get_entry(title)}),  
    })

def editAPI(request):
    if request.method == "POST":
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(request.__dict__)
        form = EditPage(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["page"])
            return HttpResponseRedirect("/"+form.cleaned_data["title"])
        else:
            print(form.errors)
            return HttpResponseBadRequest("Bad form.")
    else:
        return HttpResponseBadRequest("Bad method.")

def randomPage(request):
    entries = util.list_entries()
    entry_length = len(entries)
    randomPageNumber = random.randint(0, entry_length-1)
    return HttpResponseRedirect(entries[randomPageNumber])