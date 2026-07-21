"""第三方应用接入示例"""
import sys
import os

# 将上层 sdk-python 目录加入路径，方便本地开发时直接 import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from recaptcha import Client, Config, FailureMode, GenerateRequest


def main():
    client = Client(Config(
        base_url="http://127.0.0.1",
        api_key="replace-with-api-key",
        timeout=3.0,
        failure_mode=FailureMode.strict_block,
    ))

    resp = client.generate(GenerateRequest(
        site_id="partner-site-a",
        type="text",
        width=320,
        extra={"device_fingerprint": "fp_example_1234567890abcdef"},
    ))

    print("captcha_id:", resp.data.get("captcha_id"))
    print("verify_ticket:", resp.data.get("verify_ticket"))


if __name__ == "__main__":
    main()
