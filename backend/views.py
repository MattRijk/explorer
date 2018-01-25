from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from backend.forms import EditUserForm, EditCategoryForm
from pins.models import Category

def index(requests):
    superUsers = User.objects.filter(is_superuser=True)
    activeUser = User.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {'superUsers':superUsers,
               'activeUsers':activeUser,
               'categories':categories}
    return render(requests, template_name='index.html', context=context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = EditUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='users/user_form.html', context={'form':form})

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('backend:index')
    return render(request, 'users/user_delete.html', {'object': user})

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = EditCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='category_form.html', context={'form':form})

# def delete_user(request, slug):
#     slug = get_object_or_404(Category, slug=slug)
#     if request.method == 'POST':
#         slug.delete()
#         return redirect('backend:index')
#     return render(request, 'category_delete.html', {'object': slug})
