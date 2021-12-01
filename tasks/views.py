from django.core import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TaskForm
from django.contrib import messages

from .models import Task

# Create your views here. 
@login_required

def taskList(request):
   
   search = request.GET.get('search')
   filter = request.GET.get('filter')
   if search:

      tasks = Task.objects.filter(title_icontains=search, user=request.user)

   elif filter:

         tasks = Task.objects.filter(done = filter, user=request.user)

   else:

   #chamar todas as tasks do bd para o template
    tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user) #e paginacão
   

   #quantas tarefas exibir por página
   paginator = Paginator(tasks_list, 5)

   page = request.GET.get('page')
   #Pegando a página actual
   tasks = paginator.get_page(page)

   return render(request, 'tasks/list.html', {'tasks':tasks})

@login_required
#Visualizador de tarefas
def taskView(request, id):
   task = get_object_or_404(Task, pk=id)
   return render (request, 'tasks/task.html', {'task':task})


# CRUD - Adicionar nova tarefa
@login_required
def newTask(request):
   if request.method == 'POST':
      form = TaskForm(request.POST)

      if form.is_valid():
         task = form.save(commit=False)
         task.done = 'doing'
         task.user = request.user
         task.save()
         return redirect('/')
   else:
      form = TaskForm()
      return render (request, 'tasks/addtask.html', {'form': form})

# CRUD - UPDATE e E editar tarefa
@login_required
def editTask(request,id):
   task = get_object_or_404(Task, pk=id)
   form = TaskForm(instance=task)

   if (request.method == 'POST'):
      form = TaskForm(request.POST, instance=task)

      if (form.is_valid()):
         task.save()
         return redirect('/')
         
      else:
         return render (request, 'tasks/edittask.html', {'form': form, 'task':task})
   else:
       return render (request, 'tasks/edittask.html', {'form': form, 'task':task})

# CRUD - Delete task
@login_required
def deleteTask(request, id):
   task = get_object_or_404(Task, pk=id)
   task.delete()

   messages.info(request, 'Tarefa eliminada com sucesso!')

   return redirect('/')

   
@login_required
def changeStatus(request, id):
   task = get_object_or_404(Task, pk=id)

   if(task.done == 'doing'):
      task.done = 'done'
   else:
      task.done = 'doing'

   task.save()

   return redirect('/')

#####
def helloworld(request):
    return HttpResponse('Olá Mundo, O meu nome é Malingas Cumbane')
    
def yourName(request, name):
   return render(request, 'tasks/yourname.html ', {'name': name})


#url, view, template