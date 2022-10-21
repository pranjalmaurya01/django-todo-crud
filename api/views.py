from rest_framework import views
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login as loginUser, logout

from api.forms import TodoForm
from api.models import Todo

# Create your views here.


class SignUpView(views.APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        user_form = UserCreationForm()
        context = {"user_form": user_form}
        return Response(context, template_name='signup.html')

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        context = {
            "user_form": user_form
        }
        if user_form.is_valid():
            user = user_form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return Response(context, template_name='signup.html')


class Login(views.APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            "form": login_form
        }
        return Response(context, template_name='login.html')

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return Response(context, template_name='login.html')


class Home(LoginRequiredMixin, views.APIView):
    login_url = '/login/'
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        form = TodoForm()
        user = request.user
        todos = Todo.objects.filter(user=user).order_by("-priority")
        context = {
            "form": form,
            "todos": todos
        }
        return Response(context, template_name='home.html')


class Logout(LoginRequiredMixin, views.APIView):
    login_url = '/login/'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return redirect('login')


class AddTodo(LoginRequiredMixin, views.APIView):
    login_url = "/login"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        form = TodoForm(request.POST)
        user = request.user
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect("home")
        context = {'form': form}
        return Response(context, template_name='index.html')


class ChangeTodoStatus(LoginRequiredMixin, views.APIView):
    login_url = "/login"
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        status = kwargs.get("status")
        todo = Todo.objects.get(pk=pk)
        todo.status = status
        todo.save()
        return redirect('home')


class DeleteTodo(LoginRequiredMixin, views.APIView):
    login_url = "/login"
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return redirect('home')
