from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Sequence

from langchain_litellm import ChatLiteLLM
from litellm import acompletion, completion


DEFAULT_OPENROUTER_MODEL = "openrouter/openai/gpt-4.1-mini"
DEFAULT_OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

Message = dict[str, Any]


class MissingLLMConfiguration(RuntimeError):
    pass


@dataclass(frozen=True)
class LLMConfig:
    model: str = DEFAULT_OPENROUTER_MODEL
    api_key: str | None = None
    api_base: str = DEFAULT_OPENROUTER_API_BASE
    site_url: str | None = None
    app_name: str | None = None
    temperature: float | None = 0.2
    max_tokens: int | None = None
    timeout: float | None = 60.0

    @classmethod
    def from_env(cls, model: str | None = None) -> "LLMConfig":
        return cls(
            model=normalize_openrouter_model(
                model or os.getenv("OPENROUTER_MODEL") or DEFAULT_OPENROUTER_MODEL
            ),
            api_key=os.getenv("OPENROUTER_API_KEY"),
            api_base=os.getenv("OPENROUTER_API_BASE", DEFAULT_OPENROUTER_API_BASE),
            site_url=os.getenv("OR_SITE_URL"),
            app_name=os.getenv("OR_APP_NAME"),
            temperature=_optional_float(os.getenv("LLM_TEMPERATURE"), 0.2),
            max_tokens=_optional_int(os.getenv("LLM_MAX_TOKENS")),
            timeout=_optional_float(os.getenv("LLM_TIMEOUT"), 60.0),
        )


def _optional_float(value: str | None, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    return float(value)


def _optional_int(value: str | None, default: int | None = None) -> int | None:
    if value is None or value == "":
        return default
    return int(value)


def normalize_openrouter_model(model: str) -> str:
    clean_model = model.strip()
    if not clean_model:
        raise ValueError("LLM model is required.")
    if clean_model.startswith("openrouter/"):
        return clean_model
    return f"openrouter/{clean_model}"


def _extract_text(response: Any) -> str:
    choices = getattr(response, "choices", None)
    if choices is None and isinstance(response, dict):
        choices = response.get("choices", [])
    if not choices:
        return ""

    choice = choices[0]
    message = getattr(choice, "message", None)
    if message is None and isinstance(choice, dict):
        message = choice.get("message")

    content = getattr(message, "content", None)
    if content is None and isinstance(message, dict):
        content = message.get("content")

    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    return "" if content is None else str(content)


class LLMService:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig.from_env()
        self._validate()
        self._apply_openrouter_env()

    def _validate(self) -> None:
        if not self.config.api_key:
            raise MissingLLMConfiguration("OPENROUTER_API_KEY is required.")

    def _apply_openrouter_env(self) -> None:
        os.environ.setdefault("OPENROUTER_API_KEY", self.config.api_key or "")
        os.environ.setdefault("OPENROUTER_API_BASE", self.config.api_base)
        if self.config.site_url:
            os.environ.setdefault("OR_SITE_URL", self.config.site_url)
        if self.config.app_name:
            os.environ.setdefault("OR_APP_NAME", self.config.app_name)

    def _request_kwargs(self, **overrides: Any) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.config.model,
            "api_key": self.config.api_key,
            "base_url": self.config.api_base,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "timeout": self.config.timeout,
        }
        kwargs.update(overrides)
        return {key: value for key, value in kwargs.items() if value is not None}

    def raw_chat(self, messages: Sequence[Message], **kwargs: Any) -> Any:
        return completion(messages=list(messages), **self._request_kwargs(**kwargs))

    async def araw_chat(self, messages: Sequence[Message], **kwargs: Any) -> Any:
        return await acompletion(messages=list(messages), **self._request_kwargs(**kwargs))

    def chat(self, messages: Sequence[Message], **kwargs: Any) -> str:
        return _extract_text(self.raw_chat(messages, **kwargs))

    async def achat(self, messages: Sequence[Message], **kwargs: Any) -> str:
        return _extract_text(await self.araw_chat(messages, **kwargs))

    def complete(
        self,
        prompt: str,
        system: str | None = None,
        **kwargs: Any,
    ) -> str:
        messages: list[Message] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages, **kwargs)

    async def acomplete(
        self,
        prompt: str,
        system: str | None = None,
        **kwargs: Any,
    ) -> str:
        messages: list[Message] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return await self.achat(messages, **kwargs)


def create_llm_service(model: str | None = None) -> LLMService:
    return LLMService(LLMConfig.from_env(model=model))


def create_langchain_chat_model(
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> ChatLiteLLM:
    config = LLMConfig.from_env(model=model)
    if not config.api_key:
        raise MissingLLMConfiguration("OPENROUTER_API_KEY is required.")

    return ChatLiteLLM(
        model=config.model,
        openrouter_api_key=config.api_key,
        api_base=config.api_base,
        temperature=config.temperature if temperature is None else temperature,
        max_tokens=config.max_tokens if max_tokens is None else max_tokens,
        request_timeout=config.timeout,
        **kwargs,
    )
