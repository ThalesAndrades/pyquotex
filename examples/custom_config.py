# examples/custom_config.py

import asyncio
import logging

from pyquotex.config import credentials
from pyquotex.stable_api import Quotex

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"


def make_client() -> Quotex:
    """Build a configured Quotex client (credentials resolved at call time)."""
    # Credentials come from PYQUOTEX_EMAIL/PYQUOTEX_PASSWORD env vars
    # or settings/config.ini (never hardcode them in source).
    email, password = credentials()

    client = Quotex(
        email=email,
        password=password
    )

    # client.set_session(user_agent=USER_AGENT)
    client.set_session(
        user_agent="Mozilla/5.0...",
        cookies="seus_cookies",  # Opcional
        ssid="seu_ssid"  # Opcional
    )

    # PRACTICE mode is default / REAL mode is optional
    # client.set_account_mode("REAL")

    client.debug_ws_enable = False
    return client


async def main():
    client = make_client()
    await client.connect()
    is_connected = client.check_connect()
    if is_connected:
        print(f"Connected: {is_connected}")
        balance = await client.get_balance()
        print(f"Balance: {balance}")
    print("Saindo...")
    client.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Encerrando o programa.")
    finally:
        loop.close()
