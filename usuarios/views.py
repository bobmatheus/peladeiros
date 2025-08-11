# usuarios/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from reservas.services import authenticate, ApiError

class LoginView(View):
    def get(self, request):
        next_url = request.GET.get('next', '/')
        return render(request, 'usuarios/login.html', {'next': next_url})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or '/'
        try:
            tokens = authenticate(username, password)
        except ApiError as e:
            messages.error(request, f"Login falhou: {e}")
            return redirect('usuarios:login')
        # Esperado: tokens['access']
        access = tokens.get('access') or tokens.get('token')  # compatível com variações
        if not access:
            messages.error(request, "Resposta de autenticação inesperada.")
            return redirect('usuarios:login')
        request.session['access'] = access
        # opcional: refresh
        if tokens.get('refresh'):
            request.session['refresh'] = tokens['refresh']
        messages.success(request, "Bem-vindo! Bora jogar aquela pelada.")
        return redirect(next_url)

class LogoutView(View):
    def post(self, request):
        request.session.pop('access', None)
        request.session.pop('refresh', None)
        messages.info(request, "Você saiu da sessão.")
        return redirect('reservas:home')