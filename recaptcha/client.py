"""recaptcha SDK 客户端"""

import json
import warnings
from typing import Any, Dict, List, Optional, Tuple

import urllib3

from .types import (
    Config,
    Envelope,
    ErrorKind,
    ERROR_ENUM_BANNED,
    FailureMode,
    GenerateRequest,
    SDKError,
    VerifyRequest,
)

# 禁用 SSL 警告（内网调用场景）
urllib3.disable_warnings()
warnings.filterwarnings("ignore", message=".*urllib3 v2.*")


def normalize_clicks(points: List[Tuple[int, int]]) -> List[Dict[str, int]]:
    """坐标序列标准化：将 [(x,y), ...] 转为 [{"x": x, "y": y}, ...]"""
    return [{"x": p[0], "y": p[1]} for p in points]


def _is_banned_envelope(env: Envelope) -> bool:
    """判断响应是否为业务封禁"""
    if env.code == 1002:
        return True
    if not env.data:
        return False
    if env.data.get("ban_blocked") in (True, 1, "1", "true", "True"):
        return True
    if str(env.data.get("error_enum", "")).strip().upper() == ERROR_ENUM_BANNED.upper():
        return True
    return False


class Client:
    """recaptcha 客户端，用于调用开放平台的生成和校验接口"""

    GENERATE_PATH = "/saas/sdk/v1/recaptcha/secure/generate"
    VERIFY_PATH = "/saas/sdk/v1/recaptcha/secure/verify"

    def __init__(self, config: Config):
        self._cfg = config
        timeout = urllib3.Timeout(connect=config.timeout, read=config.timeout)
        self._http = urllib3.PoolManager(
            timeout=timeout,
            retries=False,
            cert_reqs='CERT_NONE',
        )

    def generate(self, req: GenerateRequest) -> Envelope:
        """调用开放平台接口生成验证码"""
        payload: Dict[str, Any] = {"site_id": req.site_id}
        if req.type.strip():
            payload["type"] = req.type
        if req.width > 0:
            payload["width"] = req.width
        payload.update(req.extra)
        return self._post_json(self.GENERATE_PATH, payload)

    def verify(self, req: VerifyRequest) -> Envelope:
        """调用开放平台接口二次校验"""
        payload: Dict[str, Any] = {
            "captcha_id": req.captcha_id,
            "verify_ticket": req.verify_ticket,
            "clicks": req.clicks,
        }
        payload.update(req.extra)
        return self._post_json(self.VERIFY_PATH, payload)

    def _post_json(self, path: str, body: Dict[str, Any]) -> Envelope:
        url = f"{self._cfg.base_url}{path}"
        raw = json.dumps(body).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self._cfg.api_key,
        }
        if self._cfg.log_id_factory:
            headers["X-Log-Id"] = self._cfg.log_id_factory()

        try:
            resp = self._http.request("POST", url, body=raw, headers=headers)
        except urllib3.exceptions.TimeoutError as e:
            return self._handle_error(SDKError(ErrorKind.timeout_error, str(e)))
        except urllib3.exceptions.HTTPError as e:
            return self._handle_error(SDKError(ErrorKind.network_error, str(e)))

        try:
            raw_dict = json.loads(resp.data.decode("utf-8"))
            env = Envelope.from_dict(raw_dict)
        except (json.JSONDecodeError, ValueError) as e:
            return self._handle_error(
                SDKError(ErrorKind.upstream_error, "invalid json", code=resp.status)
            )

        if resp.status >= 500:
            return self._handle_error(
                SDKError(ErrorKind.upstream_error, env.message, code=resp.status)
            )

        if env.code != 0:
            if _is_banned_envelope(env):
                env.data.setdefault("ban_blocked", True)
                env.data.setdefault("error_enum", ERROR_ENUM_BANNED)
            raise SDKError(ErrorKind.business_error, env.message, code=env.code)

        return env

    def _handle_error(self, err: SDKError) -> Envelope:
        if self._cfg.failure_mode == FailureMode.degrade_allow:
            return Envelope(
                code=0,
                message="degraded_allow",
                data={"degraded": True},
            )
        raise err
