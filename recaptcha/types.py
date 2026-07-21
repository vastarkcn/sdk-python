"""recaptcha SDK 数据类定义"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class FailureMode(str, Enum):
    """故障策略"""
    strict_block = "strict_block"        # 严格阻断
    degrade_allow = "degrade_allow"      # 降级放行


class ErrorKind(str, Enum):
    """错误类型"""
    network_error = "network_error"
    timeout_error = "timeout_error"
    upstream_error = "upstream_error"
    business_error = "business_error"


# 业务封禁错误枚举值
ERROR_ENUM_BANNED = "E_BANNED"


class SDKError(Exception):
    """SDK 统一错误"""

    def __init__(self, kind: ErrorKind, message: str, code: int = 0):
        self.kind = kind
        self.message = message
        self.code = code
        super().__init__(f"{kind.value}: {message}")


class Config:
    """客户端配置"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 3.0,
        failure_mode: FailureMode = FailureMode.strict_block,
        log_id_factory: Optional[Callable[[], str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.failure_mode = failure_mode
        self.log_id_factory = log_id_factory


class Envelope:
    """统一响应信封"""

    def __init__(self, code: int = 0, message: str = "", data: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.data = data or {}

    @staticmethod
    def from_dict(raw: Dict[str, Any]) -> "Envelope":
        return Envelope(
            code=raw.get("code", 0),
            message=raw.get("message", ""),
            data=raw.get("data") or {},
        )


class GenerateRequest:
    """生成验证码请求"""

    def __init__(
        self,
        site_id: str,
        type: str = "",
        width: int = 0,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.site_id = site_id
        self.type = type
        self.width = width
        self.extra = extra or {}


class VerifyRequest:
    """二次校验请求"""

    def __init__(
        self,
        captcha_id: str,
        verify_ticket: str,
        clicks: List[Dict[str, int]],
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.captcha_id = captcha_id
        self.verify_ticket = verify_ticket
        self.clicks = clicks
        self.extra = extra or {}
