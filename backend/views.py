from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from backend.forms import EditUserForm, CreateUserForm, SearchForm
from pins.models import Category, Pin
from django.db.models import Q
from taggit.models import Tag
from haystack.query import SearchQuerySet

def search(request):
    form = SearchForm()
    cleaned, results, total_count = None, None, 0
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cleaned = form.cleaned_data
            if cleaned['search'].lower() == 'amsterdam':
                results = ''
                # possibly return message about searching for amsterdam
            else:
                results = SearchQuerySet().filter(content=cleaned['search']).load_all()
                total_count = results.count()
    return render(request, 'search.html', {'form':form, 'cleaned':cleaned, 'results':results, 'total_count': total_count})


# using whoosh with autocomplete
# def search_titles(request):
# def search_titles(request):
#     pins = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text')).load_all()
#     return render(request, 'search.html', {'pins': pins})

# using django Q search
# def search_titles(request):
#     if request.method == "POST":
#         search_text = request.POST['search_text']
#     pins = Pin.objects.filter(Q(title__contains=search_text) | Q(tags__name__in=[search_text]))
#     return render(request, 'search.html', {'pins':pins})

@login_required(login_url="/accounts/login/")
@csrf_protect
def index(request):
    superUsers = User.objects.filter(is_superuser=True)
    activeUser = User.objects.filter(is_active=True)
    categories = Category.objects.all()
    form = SearchForm()
    context = {'superUsers':superUsers,
               'activeUsers':activeUser,
               'categories':categories,
               'form':form}

    return render(request, template_name='index.html', context=context)

@login_required(login_url="/accounts/login/")
def create_user(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='users/user_form.html', context={'form':form})

@login_required(login_url="/accounts/login/")
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = EditUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='users/user_form.html', context={'form':form})

@login_required(login_url="/accounts/login/")
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('backend:index')
    return render(request, 'users/user_delete.html', {'object': user})

