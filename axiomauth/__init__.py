"""
AxiomAuth Python SDK
https://axiomauth.com/docs
"""

from __future__ import annotations
import httpx
from typing import Any

__version__ = "1.3.1"
__all__ = ["AxiomAuth", "AxiomAuthError"]

BASE_URL = "https://api.axiomauth.com/v1"


class AxiomAuthError(Exception):
    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


class _Resource:
    def __init__(self, client: "AxiomAuth"):
        self._c = client


class _Users(_Resource):
    def list(self, **params): return self._c._get("/users", params)
    def get(self, user_id: str): return self._c._get(f"/users/{user_id}")
    def deprovision(self, user_id: str): return self._c._delete(f"/users/{user_id}")


class _Sessions(_Resource):
    def list(self, **params): return self._c._get("/sessions", params)
    def revoke(self, session_id: str): return self._c._delete(f"/sessions/{session_id}")


class _Config(_Resource):
    def get(self): return self._c._get("/config")
    def update(self, data: dict): return self._c._patch("/config", data)


class _Audit(_Resource):
    def list(self, **params): return self._c._get("/audit", params)


class AxiomAuth:
    """Synchronous AxiomAuth client."""

    def __init__(self, api_key: str, base_url: str = BASE_URL, timeout: float = 10.0):
        if not api_key:
            raise ValueError("api_key is required")
        self._http = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "User-Agent": f"axiomauth-python/{__version__}",
            },
            timeout=timeout,
        )
        self.users = _Users(self)
        self.sessions = _Sessions(self)
        self.config = _Config(self)
        self.audit = _Audit(self)

    def _request(self, method: str, path: str, params=None, json=None):
        res = self._http.request(method, path, params=params, json=json)
        if res.is_error:
            raise AxiomAuthError(f"API error {res.status_code}", res.status_code, res.text)
        return res.json()

    def _get(self, path, params=None):    return self._request("GET",    path, params=params)
    def _post(self, path, data):          return self._request("POST",   path, json=data)
    def _patch(self, path, data):         return self._request("PATCH",  path, json=data)
    def _delete(self, path):              return self._request("DELETE", path)

    def close(self): self._http.close()
    def __enter__(self): return self
    def __exit__(self, *_): self.close()
