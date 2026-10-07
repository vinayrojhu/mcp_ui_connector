"""Local Playwright worker boundary. This worker accepts only validated declarative actions."""
from typing import Any


class BrowserWorker:
    def __init__(self, page: Any, allowed_domains: set[str]):
        self.page = page
        self.allowed_domains = allowed_domains

    async def inspect(self) -> dict:
        controls = await self.page.locator("input,button,a,select,textarea").evaluate_all(
            "els => els.map((e,i) => ({index:i, tag:e.tagName.toLowerCase(), role:e.getAttribute('role'), "
            "label:e.getAttribute('aria-label') || e.labels?.[0]?.innerText || null, "
            "text:(e.innerText || '').slice(0,120), test_id:e.getAttribute('data-testid'), "
            "sensitive: /password|token|secret/i.test((e.type||'')+' '+(e.name||''))}))")
        for control in controls:
            control.pop("value", None)
        return {"url": self.page.url, "title": await self.page.title(), "controls": controls}

    async def execute_step(self, step: dict):
        target = step.get("target") or {}
        if step["type"] == "navigate":
            url = step.get("value", "")
            from urllib.parse import urlparse
            if urlparse(url).hostname not in self.allowed_domains:
                raise PermissionError("Navigation domain is blocked")
            await self.page.goto(url)
            return
        locator = None
        if target.get("test_id"):
            locator = self.page.get_by_test_id(target["test_id"])
        elif target.get("role") and target.get("name"):
            locator = self.page.get_by_role(target["role"], name=target["name"], exact=True)
        elif target.get("label"):
            locator = self.page.get_by_label(target["label"], exact=True)
        elif target.get("text"):
            locator = self.page.get_by_text(target["text"], exact=True)
        if locator is None:
            raise ValueError("Target has no supported accessible locator")
        if await locator.count() != 1:
            raise ValueError("Target is missing or ambiguous")
        if not await locator.is_visible() or not await locator.is_enabled():
            raise ValueError("Target is not actionable")
        if step["type"] == "click": await locator.click()
        elif step["type"] == "fill": await locator.fill(step.get("value", ""))
        elif step["type"] == "press": await locator.press(step.get("value", "Enter"))
        elif step["type"] == "wait": await locator.wait_for(state="visible")
        elif step["type"] == "download": raise NotImplementedError("Download handling is not enabled in the MVP")
