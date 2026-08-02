import httpx


async def fetch_balance(api_base: str) -> dict:
    async with httpx.AsyncClient(base_url=api_base, timeout=10.0) as client:
        response = await client.get("/balance")
        response.raise_for_status()
        return response.json()


async def fetch_ticks(api_base: str) -> list[dict]:
    async with httpx.AsyncClient(base_url=api_base, timeout=10.0) as client:
        response = await client.get("/ticks")
        response.raise_for_status()
        return response.json()
