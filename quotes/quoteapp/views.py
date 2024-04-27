from django.shortcuts import render,redirect, get_object_or_404
from .forms import QuoteForm, AuthorForm
from django.contrib.auth.decorators import login_required
from .models import Quote
def detail(request, quote_id):
    quote=get_object_or_404(Quote,pk=quote_id)
    return render(request,'quoteapp/detail.html', {'quote': quote})

def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quoteapp/index.html', {"quotes": quotes})

def delete_quote(request,quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect('quoteapp:main')


# Create your views here.
#
@login_required
def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request,'quoteapp/quote.html', {'form': form})

    return render(request,'quoteapp/quote.html', {'form': QuoteForm()})

@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/author.html', {'form': form})

    return render(request, 'quoteapp/author.html',{'form': AuthorForm()})

