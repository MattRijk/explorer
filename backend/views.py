from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from backend.forms import EditUserForm

def index(requests):
    superUsers = User.objects.filter(is_superuser=True)
    activeUser = User.objects.filter(is_active=True)
    context = {'superUsers':superUsers,
               'activeUsers':activeUser}
    return render(requests, template_name='index.html', context=context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = EditUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('backend:index')
    return render(request, template_name='user_form.html', context={'form':form})

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('backend:index')
    return render(request, 'delete.html', {'object': user})