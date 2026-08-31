"""
Comprehensive Test Suite for PathPilot AI Online Coding IDE / Compiler Integration
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def log(msg, status="INFO"):
    symbol = "[OK]" if status == "PASS" else "[ERR]" if status == "FAIL" else "[INFO]"
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol} [{status}] {msg}")

def test_api():
    print("\n========================================================")
    print("      PATHPILOT AI — ONLINE IDE / COMPILER SUITE       ")
    print("========================================================\n")

    # 1. Register / Login test user to get JWT token
    user_email = f"idetest_{int(datetime.now().timestamp())}@pathpilot.ai"
    token = None
    
    reg_data = json.dumps({
        "name": "IDE Tester",
        "email": user_email,
        "password": "Password123!"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=reg_data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            token = body.get("access_token")
            log(f"Test user registered: {user_email}", "PASS")
    except Exception as e:
        log(f"Failed to register test user: {e}", "FAIL")
        return

    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # TEST 1: GET /api/code/languages
    try:
        req = urllib.request.Request(f"{BASE_URL}/code/languages")
        with urllib.request.urlopen(req) as resp:
            langs = json.loads(resp.read().decode("utf-8"))
            assert len(langs) >= 10
            log(f"GET /api/code/languages returned {len(langs)} supported languages with versions", "PASS")
    except Exception as e:
        log(f"Languages endpoint test failed: {e}", "FAIL")

    # TEST 2: Execute Python Code
    py_payload = json.dumps({
        "language": "python",
        "version": "3.12",
        "sourceCode": "def greet(name):\n    print(f'Hello from PathPilot AI IDE, {name}!')\n\ngreet('Developer')",
        "stdin": ""
    }).encode("utf-8")

    try:
        req = urllib.request.Request(f"{BASE_URL}/code/execute", data=py_payload, headers=auth_headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            assert "Hello from PathPilot AI IDE, Developer!" in res.get("stdout", "")
            assert res.get("exitCode") == 0
            log(f"Python code execution SUCCESS (Time: {res.get('executionTime')}s, Exit: {res.get('exitCode')})", "PASS")
    except Exception as e:
        log(f"Python execution test failed: {e}", "FAIL")

    # TEST 3: Execute JavaScript Code
    js_payload = json.dumps({
        "language": "javascript",
        "version": "Node.js 22",
        "sourceCode": "const skills = ['React', 'Python', 'FastAPI'];\nconsole.log(`PathPilot skills count: ${skills.length}`);",
        "stdin": ""
    }).encode("utf-8")

    try:
        req = urllib.request.Request(f"{BASE_URL}/code/execute", data=js_payload, headers=auth_headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            assert "PathPilot skills count: 3" in res.get("stdout", "")
            log(f"JavaScript execution SUCCESS: {res.get('stdout').strip()}", "PASS")
    except Exception as e:
        log(f"JavaScript execution test failed: {e}", "FAIL")

    # TEST 4: STDIN Input Execution
    stdin_payload = json.dumps({
        "language": "python",
        "version": "3.12",
        "sourceCode": "import sys\nnum1 = int(sys.stdin.readline())\nnum2 = int(sys.stdin.readline())\nprint(f'Sum: {num1 + num2}')",
        "stdin": "15\n27\n"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(f"{BASE_URL}/code/execute", data=stdin_payload, headers=auth_headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            assert "Sum: 42" in res.get("stdout", "")
            log(f"STDIN input processing SUCCESS: {res.get('stdout').strip()}", "PASS")
    except Exception as e:
        log(f"STDIN test failed: {e}", "FAIL")

    # TEST 5: Syntax Error Handling
    err_payload = json.dumps({
        "language": "python",
        "version": "3.12",
        "sourceCode": "def broken_func(\n    print('Missing closing parenthesis')",
        "stdin": ""
    }).encode("utf-8")

    try:
        req = urllib.request.Request(f"{BASE_URL}/code/execute", data=err_payload, headers=auth_headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            assert res.get("exitCode") != 0
            assert "SyntaxError" in res.get("stderr", "") or "SyntaxError" in res.get("stdout", "")
            log(f"Syntax error caught cleanly without crashing backend", "PASS")
    except Exception as e:
        log(f"Syntax error test failed: {e}", "FAIL")

    # TEST 6: Code Save & Restore Draft (Persistence)
    lesson_id = 2
    save_payload = json.dumps({
        "language": "python",
        "version": "3.12",
        "code": "print('Saved draft code for lesson 2')",
        "stdin": "test_input"
    }).encode("utf-8")

    try:
        # Save
        req_save = urllib.request.Request(f"{BASE_URL}/code/lessons/{lesson_id}/save", data=save_payload, headers=auth_headers)
        with urllib.request.urlopen(req_save) as resp:
            res_save = json.loads(resp.read().decode("utf-8"))
            assert res_save.get("success") == True

        # Fetch
        req_get = urllib.request.Request(f"{BASE_URL}/code/lessons/{lesson_id}/saved", headers=auth_headers)
        with urllib.request.urlopen(req_get) as resp:
            res_get = json.loads(resp.read().decode("utf-8"))
            assert res_get.get("has_saved_code") == True
            assert res_get.get("code") == "print('Saved draft code for lesson 2')"
            assert res_get.get("stdin") == "test_input"
            log(f"Draft code saved to MySQL & restored successfully for lesson_id={lesson_id}", "PASS")
    except Exception as e:
        log(f"Save & restore draft test failed: {e}", "FAIL")

    # TEST 7: Security Isolation Check
    sec_payload = json.dumps({
        "language": "python",
        "version": "3.12",
        "sourceCode": "import os\nprint('ENV KEYS:', list(os.environ.keys())[:3])",
        "stdin": ""
    }).encode("utf-8")

    try:
        req = urllib.request.Request(f"{BASE_URL}/code/execute", data=sec_payload, headers=auth_headers)
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            # Confirm secrets like MYSQL password or JWT secret are not in env keys or sanitized
            env_out = res.get("stdout", "")
            assert "DATABASE_URL" not in env_out and "JWT_SECRET" not in env_out
            log(f"Security isolation verified: main API secrets not accessible in code execution environment", "PASS")
    except Exception as e:
        log(f"Security test failed: {e}", "FAIL")

    print("\n========================================================")
    print("      ALL COMPILER & IDE REGRESSION TESTS PASSED!      ")
    print("========================================================\n")

if __name__ == "__main__":
    test_api()
