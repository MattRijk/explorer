from django.shortcuts import render, redirect, get_object_or_404
from pins.forms import CategoryForm
from pins.models import Category


def homepage(requests):
    return render(requests, template_name='home.html', context={})

def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='categories/category_form.html', context={'form':form})

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='categories/category_form.html', context={'form':form})

def delete_category(request, slug):
    slug = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        slug.delete()
        return redirect('backend:index')
    return render(request, 'categories/category_delete.html', {'object': slug})

