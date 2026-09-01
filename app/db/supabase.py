"""Supabase client wrapper for future database integration."""


class SupabaseClient:
    def __init__(self, url: str | None = None, key: str | None = None):
        self.url = url
        self.key = key

    def ping(self) -> dict[str, str]:
        return {"status": "not_configured"}
