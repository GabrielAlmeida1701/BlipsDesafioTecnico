import httpx

EXTERNAL_URL = "https://dummyjson.com/users/1"

async def fetch_birth_date() -> str | None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(EXTERNAL_URL)
            resp.raise_for_status()
            data = resp.json()
            # The external API supplies `birthDate` according to the spec
            birth = data.get("birthDate") or data.get("birth_date") or data.get("birth")
            return birth
    except Exception:
        # On any failure return None (documented behaviour in README)
        return None
