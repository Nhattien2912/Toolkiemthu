import os


BASE_URL = os.getenv("BASE_URL", "https://guangli-shop.netlify.app/")
API_BASE_URL = os.getenv("API_BASE_URL", "https://web-mern-t10-2024.onrender.com")

INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_password"

SUCCESS_LOGIN_MESSAGE = "Đăng nhập thành công."
INVALID_LOGIN_MESSAGE = "Tên đăng nhập, số điện thoại hoặc mật khẩu không đúng."
