from django.shortcuts import render
from markdown2 import markdown
from . import util
from .forms import NewEntryForm
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

# Index page which shows a list of entries
def index(request):
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Page for individual entry. 
def entry(request, title):
    # Gets entry from entries dir
    entry = util.get_entry(title)
    # If entry does not exist, return not found page
    if not entry:
        return render(request, "encyclopedia/notfound.html", {
            'title': title
        })
    # If entry does exist, render to html
    entry_adjusted = markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'entry': entry_adjusted
    })


# Search for entries, returning entry if exact match, or list of entries with partial matches.
def search(request):
    query = request.GET.get('q', '')
    if query in util.list_entries():
        return HttpResponseRedirect(reverse("entry", kwargs={'title': query}))
    else:
        results = []

        for entry in util.list_entries():
            if query in entry:
                results.append(entry)


        return render(request, 'encyclopedia/search.html', {
            'results': results,
            'query': query
        })


def new_page(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            # Check for post already in dir
            title = form.cleaned_data['title']
            if util.get_entry(title) == None:
                # If user is not in dir, add markdown file to entries and redirect to the new page
                util.save_entry(title, form.cleaned_data['body'])
                return HttpResponseRedirect(reverse("entry", kwargs={ 'title': title }))
            # Else show error message
            else:
                return render(request, 'encyclopedia/error.html', { 'title': title })


    return render(request, 'encyclopedia/new-page.html', {
        'form': NewEntryForm()
    })


def edit(request, title):

    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
        
            # If user is not in dir, add markdown file to entries and redirect to the new page
            util.save_entry(title, form.cleaned_data['body'])
            return HttpResponseRedirect(reverse("entry", kwargs={ 'title': title }))

    else:
        # Gets entry from entries dir
        entry = util.get_entry(title)
        #prepopulate form with entry info
        form = NewEntryForm({ 'title': title, 'body': entry })
        return render(request, "encyclopedia/edit.html", {
            'form': form,
            'title': title
        })


def random_entry(request):
    entries = util.list_entries()
   
   
    return HttpResponseRedirect(reverse("entry", kwargs={ 'title': random.choice(entries) }))