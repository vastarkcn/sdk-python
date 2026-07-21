# vastark recaptcha Python SDK

## 安装

```bash
pip install -e /path/to/sdk-python
```

依赖：`urllib3 >= 1.26.0`，无其他第三方依赖。

## 快速开始

```python
from recaptcha import Client, Config, FailureMode, GenerateRequest

client = Client(Config(
    base_url="http://127.0.0.1:8090",
    api_key="your-api-key",
    failure_mode=FailureMode.strict_block,
))

resp = client.generate(GenerateRequest(
    site_id="partner-site-a",
    type="text",
    width=320,
    extra={"device_fingerprint": "fp_xxx"},
))

print(resp.data["captcha_id"])
print(resp.data["verify_ticket"])
```

## 核心能力

- `Client.generate(req)` — 调用开放平台接口生成验证码（后端使用）
- `Client.verify( req)` — 调用开放平台接口二次校验（后端使用）
- `GenerateRequest.extra` / `VerifyRequest.extra` — 可透传扩展字段（例如 `device_fingerprint`）
- `normalize_clicks(points)` — 坐标序列标准化：`[(x,y), ...]` → `[{"x": x, "y": y}, ...]`
- `X-Log-Id` 自动透传（通过 `Config.log_id_factory` 回调）
- 业务封禁可感知：`error_enum=E_BANNED`（在 `SDKError` 异常中抛出）
- 故障策略：
  - `strict_block`（严格阻断，默认）
  - `degrade_allow`（降级放行，返回 `{"degraded": true}` 的 `Envelope`）
  - 约束：`degrade_allow` 仅用于服务不可用场景；`E_BANNED` 不属于放行条件

## 声明条款

1. 商业授权与 API 调用：
本项目采用 MIT/Apache-2.0 协议开源。使用本项目代码连接到官方 API 服务，不受本协议限制，仅需遵循服务条款。

2. 本地运行与修改：
允许任何人下载、修改、自用本项目代码。但若您将修改后的代码作为商业产品对外分发（例如打包成 SaaS 售卖、或封装成闭源插件），请务必联系我们获得商业豁免或授权（或说明必须保留我的版权信息）。

3. 免责条款：
本软件按"现状"提供，作者不对因使用本代码导致的任何数据丢失、服务器故障或法律纠纷承担任何责任。
