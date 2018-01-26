from django.shortcuts import render, redirect, get_object_or_404
from backend.forms import EditCategoryForm
from pins.models import Category


def homepage(requests):
    return render(requests, template_name='home.html', context={})

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = EditCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='category_form.html', context={'form':form})

def delete_category(request, slug):
    slug = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        slug.delete()
        return redirect('backend:index')
    return render(request, 'category_delete.html', {'object': slug})

