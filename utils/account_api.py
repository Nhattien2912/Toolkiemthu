import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from random import randint

from config import API_BASE_URL


@dataclass
class TestAccount:
    username: str
    password: str
    full_name: str
    phone: str


@dataclass
class AuthenticatedAccount(TestAccount):
    user_id: str
    token: str
    storage_user_json: str


def create_test_account():
    unique_id = f"{int(time.time())}{randint(100, 999)}"
    username = f"testselenium{unique_id[-9:]}"
    password = "Abcd123@"
    phone = f"09{unique_id[-8:]}"

    payload = {
        "username": username,
        "phone": phone,
        "fullName": "Selenium Test User",
        "password": password,
        "confirmPassword": password,
    }

    request = urllib.request.Request(
        url=f"{API_BASE_URL}/api/user/signup",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        response_text = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Khong tao duoc tai khoan test: {response_text}") from error

    if response.status not in (200, 201):
        raise RuntimeError(f"Tao tai khoan test that bai: HTTP {response.status}")

    return TestAccount(
        username=data["user"]["username"],
        password=password,
        full_name=data["user"]["fullName"],
        phone=data["user"]["phone"],
    )


def sign_in_test_account(username_or_phone, password):
    payload = {
        "usernameOrPhone": username_or_phone,
        "password": password,
    }

    request = urllib.request.Request(
        url=f"{API_BASE_URL}/api/user/signin",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        response_text = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Khong dang nhap duoc tai khoan test: {response_text}") from error

    if response.status != 200 or not data.get("success"):
        raise RuntimeError("Dang nhap tai khoan test that bai.")

    return data


def create_authenticated_account():
    account = create_test_account()
    login_data = sign_in_test_account(account.username, account.password)
    user = login_data["user"]
    storage_user = {
        "username": user["username"],
        "fullName": user["fullName"],
        "phone": user["phone"],
        "avatar": user.get("avatar", ""),
        "userId": user["_id"],
    }

    return AuthenticatedAccount(
        username=account.username,
        password=account.password,
        full_name=account.full_name,
        phone=account.phone,
        user_id=user["_id"],
        token=login_data["token"],
        storage_user_json=json.dumps(storage_user, ensure_ascii=False),
    )
