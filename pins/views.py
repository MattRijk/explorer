from django.shortcuts import render, redirect, get_object_or_404
from pins.forms import CategoryForm, PinForm
from pins.models import Category, Pin


def homepage(requests):
    categories = Category.objects.all()
    return render(requests, template_name='home.html', context={'categories': categories})

def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('backend:categories')
    return render(request, template_name='categories/category_form.html', context={'form':form})

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('backend:categories')
    return render(request, template_name='categories/category_form.html', context={'form':form})

def delete_category(request, slug):
    slug = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        slug.delete()
        return redirect('backend:categories')
    return render(request, 'categories/category_delete.html', {'object':slug})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories':categories})

def pins_list(request):
    pins = Pin.objects.all()
    return render(request, 'pins/pins_list.html', {'pins':pins})

def create_pin(request):
    form = PinForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('backend:pins_list')
    return render(request, template_name='pins/pins_form.html', context={'form':form})

def edit_pin(request, slug):
    pin = get_object_or_404(Pin, slug=slug)
    form = PinForm(request.POST or None, request.FILES or None,  instance=pin)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        return redirect('backend:pins_list')
    return render(request, template_name='pins/pins_form.html', context={'form':form})
