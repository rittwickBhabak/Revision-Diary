from django.contrib import messages
from django.urls import reverse, reverse_lazy 
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
from .models import Task, ToDo 
from datetime import date, datetime, timedelta

def home(request):
    today = date.today()
    yestarday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    todo_list = ToDo.objects.filter(date=date.today())
    yestarday_todo_list = ToDo.objects.filter(date=yestarday, is_completed=False)
    tomorrow_todo_list = ToDo.objects.filter(date=tomorrow)
    return render(request, 'myapp/todo_list.html', context={'todo_list': todo_list, 'yestarday_todo_list': yestarday_todo_list, 'tomorrow_todo_list': tomorrow_todo_list })

def update_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(ToDo, pk=pk)
        todo.is_completed = not todo.is_completed
        todo.save()
        return JsonResponse({"status":f"{todo.is_completed}"})
    else:
        return HttpResponseNotAllowed('Not allowed')

def create_task(request):
    if request.method == 'GET':
        return render(request, 'myapp/task_form.html')
    else:
        date_list_string = request.POST.get('date-list-string')
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_list = date_list_string.split(',')[:-1]
        task = Task.objects.create(title=title, description=description)
        for d in date_list:
            d, m, y = list(map(int, d.split('-')))
            todo = ToDo.objects.get_or_create(task=task, date=datetime(y, m+1, d))

        return redirect(reverse('myapp:task-detail', args=[task.pk]))

class DeleteTask(DeleteView):
    model = Task 
    success_url = reverse_lazy('myapp:home')

class AllTask(ListView):
    model = Task 
    def get_queryset(self):
        return Task.objects.all().order_by('-created_at')

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    todo_list = ToDo.objects.filter(task=task).order_by('date')
    return render(request, 'myapp/task_detail.html', context={'task': task, 'todo_list': todo_list})

def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    todos = ToDo.objects.filter(task=task)
    date_list_string = ''
    if request.method == 'GET':
        for todo in todos:
            d = int(todo.date.strftime('%d'))
            m = int(todo.date.strftime('%m'))-1
            y = todo.date.strftime('%Y')
            date_list_string = date_list_string + f"{d}-{m}-{y},"
        return render(request, 'myapp/task_form.html', context={'form': {'title': task.title, 'pk': task.pk, 'date_list_string': date_list_string, 'description': task.description}})
    else:
        date_list_string = request.POST.get('date-list-string')
        title = request.POST.get('title')
        description = request.POST.get('description')
        new_date_list = date_list_string.split(',')[:-1]
        task.title = title 
        task.description = description
        task.save()
        for d in new_date_list:
            d, m, y = list(map(int, d.split('-')))
            todo = ToDo.objects.filter(task=task, date=datetime(y, m+1, d))
            if not todo:
                ToDo.objects.create(task=task, date=datetime(y, m+1, d))
        messages.success(request, 'Task Update Successfully!')
        return redirect(reverse('myapp:task-detail', args=[task.pk]))
    

def delete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(ToDo, pk=pk)
        todo.delete()
        return JsonResponse({"status": "deleted"})
    else:
        return HttpResponseNotAllowed("Not Allowed")

def on_day(request):
    d = request.GET.get('date')
    print(d)
    todo_list = ToDo.objects.filter(date=datetime.strptime(d, '%Y-%m-%d'))
    return render(request, 'myapp/on_date.html', context={'todo_list': todo_list, 'date': d})