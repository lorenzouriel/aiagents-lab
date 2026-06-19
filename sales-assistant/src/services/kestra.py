from datetime import datetime, timedelta, timezone

import httpx
import structlog

from src.config import settings

log = structlog.get_logger()


class KestraClient:
    _NAMESPACE = "sales-agent"

    def __init__(self) -> None:
        self.base_url = settings.kestra_url

    async def trigger_followup(self, phone_number: str, delay_hours: int) -> str | None:
        flow_id = f"follow-up-{delay_hours}h"
        scheduled = (
            datetime.now(tz=timezone.utc) + timedelta(hours=delay_hours)
        ).isoformat()
        return await self._execute(flow_id, {"phone_number": phone_number}, scheduled)

    async def trigger_summary(self, phone_number: str, lead_id: str) -> str | None:
        return await self._execute(
            "conversation-summary",
            {"phone_number": phone_number, "lead_id": lead_id},
        )

    async def _execute(
        self, flow_id: str, inputs: dict, scheduled_date: str | None = None
    ) -> str | None:
        url = f"{self.base_url}/api/v1/executions/{self._NAMESPACE}/{flow_id}"
        body: dict = {"inputs": inputs}
        if scheduled_date:
            body["scheduledDate"] = scheduled_date

        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(url, json=body)
                    resp.raise_for_status()
                    execution_id = resp.json().get("id")
                    log.info("kestra_triggered", flow=flow_id, execution=execution_id)
                    return execution_id
            except Exception as exc:
                if attempt == 1:
                    log.error("kestra_trigger_failed", flow=flow_id, error=str(exc))
                    return None
        return None
