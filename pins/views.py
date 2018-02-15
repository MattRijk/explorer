from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pins.forms import CategoryForm, PinForm
from pins.models import Category, Pin


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
    return render(request, template_name='pins/pins_form.html', context={'form':form})

@login_required(login_url="/login/")
def edit_pin(request, slug):
    pin = get_object_or_404(Pin, slug=slug)
    form = PinForm(request.POST or None, request.FILES or None,  instance=pin)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
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
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'categories/category_detail.html', {'category':category})

def pin_detail(request, **kwargs):
    category = get_object_or_404(Category, slug=kwargs.get('category'))
    pin = get_object_or_404(Pin, slug=kwargs.get('slug'))
    return render(request=request, template_name='pins/pin_detail.html', context={'pin':pin, 'category': category})

def all_images(request):
    pins = Pin.objects.all()
    return render(request, 'pins/all_images.html', {'pins':pins})

def pin_image(request, slug):
    pin = get_object_or_404(Pin, slug=slug)
    return render(request, 'pins/pin_detail.html', {'pin':pin})

