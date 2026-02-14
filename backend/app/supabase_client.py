from functools import lru_cache

from supabase import Client, create_client

from app.config import settings


@lru_cache
def _get_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_key)


class _LazyClient:
    """Proxy that defers Supabase client creation until first attribute access."""

    def __getattr__(self, name: str):
        return getattr(_get_client(), name)


supabase: Client = _LazyClient()  # type: ignore[assignment]
