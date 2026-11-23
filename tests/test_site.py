import os
import tempfile

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8081")


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    with tempfile.TemporaryDirectory() as profile:
        options.add_argument(f"--user-data-dir={profile}")
        browser = webdriver.Chrome(
            service=Service("/usr/bin/chromedriver"),
            options=options
        )
        try:
            yield browser
        finally:
            browser.quit()


def test_page_title(driver):
    driver.get(BASE_URL)
    assert "FA23-BCT-018" in driver.title


def test_heading(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "heading")
    assert heading.text == "DevOps CI/CD Assignment 3"


def test_greeting_button(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet").click()
    message = driver.find_element(By.ID, "message").text
    assert "Hello Muaaz!" in message


def test_text_input(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "userInput").send_keys(
        "Selenium testing successful"
    )
    driver.find_element(By.ID, "submit").click()

    output = driver.find_element(By.ID, "output").text
    assert output == "Selenium testing successful"

    driver.save_screenshot("assignment3-screenshot.png")
