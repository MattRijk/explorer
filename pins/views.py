from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pins.forms import CategoryForm, PinForm, DataForm, SearchForm
from pins.models import Category, Pin
from django.views.generic import FormView
from haystack.query import SearchQuerySet


def home_page(requests):
    categories = Category.objects.all()
    return render(requests, template_name='home.html', context={'categories': categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories':categories})

@login_required(login_url="/login/")
def create_category(request):
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('backend:admin_category_list')
    else:
        form = CategoryForm()
    return render(request, template_name='categories/category_form.html', context={'form':form})

@login_required(login_url="/login/")
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(request.POST or None, request.FILES or None,  instance=category)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        return redirect('backend:admin_category_list')
    return render(request, template_name='categories/category_form.html', context={'form':form})

@login_required(login_url="/login/")
def delete_category(request, slug):
    slug = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        slug.delete()
        return redirect('backend:admin_category_list')
    return render(request, 'categories/category_delete.html', {'object':slug})

@login_required(login_url="/login/")
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/admin_category_list.html', {'categories':categories})

@login_required(login_url="/login/")
def pins_list(request):
    pins = Pin.objects.all()
    return render(request, 'pins/pins_list.html', {'pins':pins})

@login_required(login_url="/login/")
def create_pin(request):
    form = PinForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('backend:pins_list')
    else:
        form = PinForm()
    return render(request, template_name='pins/pins_form.html', context={'form':form})

@login_required(login_url="/login/")
def edit_pin(request, slug):
    pin = get_object_or_404(Pin, slug=slug)
    form = PinForm(request.POST or None, request.FILES or None,  instance=pin)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        form.save_m2m()
        return redirect('backend:pins_list')
    return render(request, template_name='pins/pins_form.html', context={'form':form})

@login_required(login_url="/login/")
def delete_pin(request, slug):
    slug = get_object_or_404(Pin, slug=slug)
    if request.method == 'POST':
        slug.delete()
        return redirect('backend:pins_list')
    return render(request, 'pins/pin_delete.html', {'object':slug})

def category_detail(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
    except Category.MultipleObjectsReturned:
        category = Category.objects.filter(slug=slug).order_by('-published').first()
    pins = category.pin_set.order_by('-published')
    return render(request, 'categories/category_detail.html', {'category':category, 'pins':pins})

def pin_detail(request, **kwargs):
    try:
        category = get_object_or_404(Category, slug=kwargs.get('category'))
        pin = get_object_or_404(Pin, slug=kwargs.get('slug'))
    except Pin.MultipleObjectsReturned:
        pin = Pin.objects.filter(slug=kwargs.get('slug')).order_by('-published').first()
    return render(request=request, template_name='pins/pin_detail.html', context={'pin':pin, 'category': category})

def all_images(request):
    pins = Pin.objects.order_by('?') # random
    return render(request, 'pins/all_images.html', {'pins':pins})

def pin_image(request, slug):
    try:
        pin = get_object_or_404(Pin, slug=slug)
    except Pin.MultipleObjectsReturned:
        pin = Pin.objects.filter(slug=slug).order_by('-published').first()
    return render(request, 'pins/pin_detail.html', {'pin':pin})

class DataFormView(FormView):
    template_name = 'upload/csv_upload.html'
    form_class = DataForm
    success_url = '/'

    def form_valid(self, form):
        form.process_data()
        return super().form_valid(form)


def search(request):
    form = SearchForm()
    cleaned, results, total_count = None, None, 0
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cleaned = form.cleaned_data
            if cleaned['search'].lower() == 'amsterdam':
                results = ''
                messages.warning(request, 'Returned too many results.')
            else:
                results = SearchQuerySet().filter(content=cleaned['search']).load_all()
                total_count = results.count()
    return render(request, 'search.html', {'form':form, 'cleaned':cleaned, 'results':results, 'total_count': total_count})


# from django.db.models import Q
# from taggit.models import Tag
# from haystack.query import SearchQuerySet

# def search(request):
#     form = SearchForm()
#     cleaned, results, total_count = None, None, 0
#     if 'search' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             cleaned = form.cleaned_data
#             if cleaned['search'].lower() == 'amsterdam':
#                 results = ''
#                 # possibly return message about searching for amsterdam
#             else:
#                 results = SearchQuerySet().filter(content=cleaned['search']).load_all()
#                 total_count = results.count()
#     return render(request, 'search.html', {'form':form, 'cleaned':cleaned, 'results':results, 'total_count': total_count})


# using whoosh with autocomplete
# def search_titles(request):
# def search_titles(request):
#     pins = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text')).load_all()
#     return render(request, 'search_form.html', {'pins': pins})

# using django Q search
# def search_titles(request):
#     if request.method == "POST":
#         search_text = request.POST['search_text']
#     pins = Pin.objects.filter(Q(title__contains=search_text) | Q(tags__name__in=[search_text]))
#     return render(request, 'search_form.html', {'pins':pins})


