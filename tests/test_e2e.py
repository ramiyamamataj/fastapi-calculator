import pytest
import subprocess
import time
import socket
import sys

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

@pytest.fixture(scope="module", autouse=True)
def start_server():
    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"])
    timeout = 10
    start = time.time()
    while not is_port_open(8000):
        time.sleep(0.2)
        if time.time() - start > timeout:
            server.terminate()
            raise RuntimeError("Server failed to start")
    yield
    server.terminate()
    server.wait()

def test_web_ui_flow(page):
    page.goto("http://127.0.0.1:8000")
    assert page.inner_text("h1") == "FastAPI Calculator"
    
    page.fill("#num_a", "12")
    page.select_option("#operation", "add")
    page.fill("#num_b", "8")
    page.click("#calculate-btn")
    
    page.wait_for_selector("#result:has-text('Result: 20')")
    assert page.inner_text("#result") == "Result: 20"
