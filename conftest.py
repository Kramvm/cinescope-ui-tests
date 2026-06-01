import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import os

load_dotenv()


class UserData:
    def __init__(self, email, password):
        self.email = email
        self.password = password


@pytest.fixture()
def registered_user():
    return UserData(
        email=os.getenv("USER_EMAIL"),
        password=os.getenv("USER_PASSWORD")
    )


@pytest.fixture()
def ui_page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()