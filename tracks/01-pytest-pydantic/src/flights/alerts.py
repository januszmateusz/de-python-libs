import json
import os
import urllib.request


def send_alert(message: str) -> None:
    """Wysyła alert na kanał zespołu przez webhook HTTP (adres z FLIGHTS_ALERT_WEBHOOK)."""
    url = os.environ["FLIGHTS_ALERT_WEBHOOK"]
    payload = json.dumps({"text": message}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5):
        pass
