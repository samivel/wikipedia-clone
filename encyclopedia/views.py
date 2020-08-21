from django.shortcuts import render
from markdown2 import markdown
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/notfound.html", {
            'title': title
        })

    entry_adjusted = markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        'title': title,
        'entry': entry_adjusted
    })

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