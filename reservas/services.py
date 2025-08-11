# reservas/services.py
import requests
from django.conf import settings

class ApiError(Exception):
    pass

class PeladeirosAPI:
    def __init__(self, access_token=None):
        self.base = settings.API_BASE_URL.rstrip('/')
        self.timeout = settings.API_TIMEOUT
        self.ep = settings.API_ENDPOINTS
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
        if access_token:
            self.session.headers.update({'Authorization': f'Bearer {access_token}'})

    def _url(self, path):
        return f"{self.base}{path}"

    def list_campos(self, params=None):
        r = self.session.get(self._url(self.ep['campos']), params=params, timeout=self.timeout)
        if r.status_code != 200:
            raise ApiError(f"Erro list_campos: {r.status_code} {r.text}")
        return r.json()

    def get_campo(self, campo_id):
        path = self.ep['campo_detail'].format(id=campo_id)
        r = self.session.get(self._url(path), timeout=self.timeout)
        if r.status_code != 200:
            raise ApiError(f"Erro get_campo: {r.status_code} {r.text}")
        return r.json()

    def get_disponibilidade(self, campo_id, data=None, duracao_min=None, horario=None):
        path = self.ep['disponibilidade'].format(id=campo_id)
        params = {}
        if data: params['data'] = data
        if duracao_min: params['duracao_min'] = duracao_min
        if horario: params['horario'] = horario
        r = self.session.get(self._url(path), params=params, timeout=self.timeout)
        if r.status_code != 200:
            raise ApiError(f"Erro disponibilidade: {r.status_code} {r.text}")
        return r.json()

    def criar_reserva(self, payload):
        r = self.session.post(self._url(self.ep['reservas']), json=payload, timeout=self.timeout)
        if r.status_code not in (200, 201):
            raise ApiError(f"Erro criar_reserva: {r.status_code} {r.text}")
        return r.json()

def authenticate(username, password):
    ep = settings.API_ENDPOINTS['jwt_obtain']
    url = f"{settings.API_BASE_URL.rstrip('/')}{ep}"
    r = requests.post(url, json={'username': username, 'password': password}, timeout=settings.API_TIMEOUT)
    if r.status_code not in (200, 201):
        raise ApiError(f"Falha de autenticação: {r.status_code} {r.text}")
    return r.json()  # esperado: {'access': '...', 'refresh': '...'} ou similar