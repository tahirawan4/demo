from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')

        return render(request, self.template_name, {})


class LogOutView(View):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name, {})


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        groups = request.user.groups.all()
        return render(request, self.template_name, {'user': 'teacher' if groups[0].name == 'Faculty'  else 'student'})

        # def post(self, request):
        #     username = request.POST.get('username', '')
        #     password = request.POST.get('password', '')
        #     user = authenticate(username=username, password=password)
        #     if user:
        #         return redirect('contact')
        #
        #     return render(request, self.template_name, {})
