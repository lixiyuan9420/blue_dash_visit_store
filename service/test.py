import requests
import time


def get(url: str, **kwargs):
    r = requests.get(
        url,
        cookies=kwargs.get("cookies", {}),
        params=kwargs.get("params", {}),
        headers=dict(kwargs.get("headers", {}), **{"Connection": "close"}),
        json=kwargs.get("json", {}),
    )
    return r


def post(url: str, **kwargs):
    r = requests.post(
        url,
        cookies=kwargs.get("cookies", {}),
        params=kwargs.get("params", {}),
        headers=dict(kwargs.get("headers", {}), **{"Connection": "close"}),
        json=kwargs.get("json", {}),
    )
    return r


def get_tenant_header():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    # 开放平台机器人应用凭证，用于开通访问服务台权限
    body = {
        "app_id": "cli_a207337a17f9100e",
        "app_secret": "oXmHsL2k1z36Z4eHZkaijgAXzcdUuj4w"
    }
    # 把 服务台ID:服务台Token 转换为base64，填写到 X-Lark-Helpdesk-Authorization，用于指定访问哪个服务台
    # 在线base64编码  https://base64.us  https://tool.oschina.net/encrypt?type=3
    return {
        "Authorization": "Bearer %s"
                         % post(url, json=body).json()["tenant_access_token"],
        "X-Lark-Helpdesk-Authorization": "Njk4OTgwNTM1ODU1ODQ3ODM1NTpodC1lYjk1Y2ZlYi03ZGM1LTY1ZGUtMTUzOS1iMzZmOTk3MmM3ZjA=",
    }


tenant_header = get_tenant_header()


def get_ticket(id):
    url = "https://open.feishu.cn/open-apis/helpdesk/v1/tickets/%s" % id
    res = get(url, headers=tenant_header)
    try:
        info = res.json()["data"]["ticket"]
        return info
    except:
        print(id, res)
        return get_ticket(id)


info = get_ticket("工单ID")
print(info)
