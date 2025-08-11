# reservas/views_public.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from .services import PeladeirosAPI, ApiError

def _get_token(request):
    return request.session.get('access')

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class CamposListView(View):
    def get(self, request):
        params = {
            'q': request.GET.get('q') or None,
            'bairro': request.GET.get('bairro') or None,
            'data': request.GET.get('data') or None,
            'horario': request.GET.get('horario') or None,
        }
        # remove None
        params = {k: v for k, v in params.items() if v}
        api = PeladeirosAPI(access_token=_get_token(request))
        try:
            campos = api.list_campos(params=params)
        except ApiError as e:
            messages.error(request, f"Erro ao buscar campos: {e}")
            campos = []
        return render(request, 'reservas/campos_list.html', {'campos': campos, 'filtros': params})

class CampoDetailView(View):
    def get(self, request, campo_id):
        api = PeladeirosAPI(access_token=_get_token(request))
        try:
            campo = api.get_campo(campo_id)
        except ApiError as e:
            messages.error(request, f"Erro ao carregar campo: {e}")
            return redirect('home')
        return render(request, 'reservas/campo_detail.html', {'campo': campo})

class DisponibilidadeHX(View):
    # endpoint para HTMX carregar slots
    def get(self, request):
        campo_id = request.GET.get('campo_id')
        data = request.GET.get('data')
        duracao = request.GET.get('duracao_min')
        horario = request.GET.get('horario')
        if not campo_id or not data:
            return HttpResponseBadRequest("Parâmetros insuficientes.")
        api = PeladeirosAPI(access_token=_get_token(request))
        try:
            disp = api.get_disponibilidade(campo_id=int(campo_id), data=data, duracao_min=duracao, horario=horario)
        except ApiError as e:
            return HttpResponse(f"<div class='text-danger'>Erro de disponibilidade: {e}</div>")
        return render(request, 'reservas/partials/_slots.html', {'disponibilidade': disp, 'campo_id': campo_id, 'data': data})

class ReservaCheckoutView(View):
    def get(self, request):
        # Espera receber via query os dados do slot escolhido
        campo_id = request.GET.get('campo_id')
        inicio = request.GET.get('inicio')  # ex: "2025-08-12T20:00"
        fim = request.GET.get('fim')
        preco = request.GET.get('preco')
        if not all([campo_id, inicio, fim]):
            messages.warning(request, "Selecione um horário para reservar.")
            return redirect('home')
        api = PeladeirosAPI(access_token=_get_token(request))
        try:
            campo = api.get_campo(campo_id)
        except ApiError:
            campo = None
        return render(request, 'reservas/reserva_checkout.html', {
            'campo': campo, 'inicio': inicio, 'fim': fim, 'preco': preco
        })

    def post(self, request):
        if not _get_token(request):
            messages.info(request, "Faça login para concluir a reserva.")
            return redirect('usuarios:login')  # com ?next=/reservar/
        payload = {
            'campo_id': int(request.POST.get('campo_id')),
            'inicio': request.POST.get('inicio'),
            'fim': request.POST.get('fim'),
            'observacao': request.POST.get('observacao') or '',
        }
        api = PeladeirosAPI(access_token=_get_token(request))
        try:
            reserva = api.criar_reserva(payload)
        except ApiError as e:
            messages.error(request, f"Não foi possível criar a reserva: {e}")
            return redirect('home')
        request.session['ultima_reserva'] = reserva
        return redirect('reservas:confirmacao')

class ReservaConfirmacaoView(View):
    def get(self, request):
        reserva = request.session.get('ultima_reserva')
        if not reserva:
            return redirect('home')
        return render(request, 'reservas/reserva_confirmacao.html', {'reserva': reserva})