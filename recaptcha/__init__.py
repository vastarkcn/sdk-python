"""vastark recaptcha Python SDK"""

import warnings

# 提前过滤 urllib3 的 SSL 兼容性警告
warnings.filterwarnings("ignore", message=".*urllib3 v2.*")

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
from .client import Client, normalize_clicks

__all__ = [
    "Config",
    "Client",
    "Envelope",
    "ErrorKind",
    "ERROR_ENUM_BANNED",
    "FailureMode",
    "GenerateRequest",
    "normalize_clicks",
    "SDKError",
    "VerifyRequest",
]
