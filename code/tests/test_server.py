"""This file contains tests to ensure the capability and correctness of server.py
The tests are separated into groups to test different aspects of server.py.

- Number of Tests: 22

"""

import importlib

import pytest
from fastapi.testclient import TestClient
from server import app


################################################################################
# Test: /getrules                       ########################################
################################################################################


def test_get_rules_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    response = client.get("/getrules")
    assert "'response': 'True'" in str(response.json())
    assert "['4', '(* x 1)', '(x)']" in str(response.json())


def test_get_rules_2():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    client.post("/addrule", json={"lhs": "(* y 1)", "rhs": "(y)"})
    response = client.get("/getrules")
    assert "'response': 'True'" in str(response.json())
    assert "['4', '(* x 1)', '(x)']" in str(response.json())
    assert "['6', '(* y 1)', '(y)']" in str(response.json())


def test_get_rules_3():
    import server

    importlib.reload(server)
    client = TestClient(app)
    response = client.get("/getrules")
    assert "'response': 'False'" in str(response.json())


################################################################################
# Test: /addrule                        ########################################
################################################################################


def test_add_rule_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    response = client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    assert "'response': 'True'" in str(response.json())


def test_add_rule_2():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    response = client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "x)"})
    assert "'response': 'False'" in str(response.json())


################################################################################
# Test: /applyrule                      ########################################
################################################################################


def test_apply_rule_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    response = client.post("/applyrule", json={"payload": "0"})
    assert "'response': 'True'" in str(response.json())


def test_apply_rule_2():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    client.post("/addrule", json={"lhs": "(* y 1)", "rhs": "(y)"})
    response = client.post("/applyrule", json={"payload": "1"})
    assert "'response': 'True'" in str(response.json())


def test_apply_rule_3():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(/ a 2)"})
    client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    client.post("/addrule", json={"lhs": "(* y 1)", "rhs": "(y)"})
    response = client.post("/applyrule", json={"payload": "9"})
    assert "'response': 'False'" in str(response.json())


################################################################################
# Test: /uploadrules                    ########################################
################################################################################


def test_upload_rule_1():
    client = TestClient(app)
    response = client.post(
        "/uploadrules",
        json={
            "payload": '{"RewriteRules": {"0": ["0", "(* x 2)", "(<< x 1)"],"1": ["1", "(/ x x)", "(1)"],"2": ["2", "(+ x y)", "(+ y x)"]}}'
        },
    )
    assert "'response': 'True'" in str(response.json())


def test_upload_rule_2():
    client = TestClient(app)
    response = client.post(
        "/uploadrules",
        json={
            "payload": '{"rr": {"0": ["0", "(* x 2)", "(<< x 1)"],"1": ["1", "(/ x x)", "(1)"],"2": ["2", "(+ x y)", "(+ y x)"]}}'
        },
    )
    assert "'response': 'False'" in str(response.json())


################################################################################
# Test: /createegraph                   ########################################
################################################################################


def test_create_egraph_1():
    client = TestClient(app)
    response = client.post("/createegraph", json={"payload": "(+ x 1)"})
    assert response.json() == {"response": "True", "msg": "Created EGraph."}


def test_create_egraph_2():
    client = TestClient(app)
    response = client.post("/createegraph", json={"payload": "+ x 1)"})
    assert "'response': 'False'" in str(response.json())


################################################################################
# Test: /loadegraph                     ########################################
################################################################################


def test_load_egraph_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(+ x 1)"})
    response = client.get("/loadegraph")
    assert "'msg': 'EGraph loaded.'" in str(response.json())


def test_load_egraph_2():
    import server

    importlib.reload(server)
    client = TestClient(app)
    response = client.get("/loadegraph")
    print(response.json())
    assert "'response': 'False'" in str(response.json())


################################################################################
# Test: /move                           ########################################
################################################################################


def test_move_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(* x 1)"})
    response = client.post(
        "/move", json={"payload": "forward", "debugModeEnabled": "false"}
    )
    assert "'response': 'False'" in str(response.json())


def test_move_2():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(* x 1)"})
    response = client.post(
        "/move", json={"payload": "fastforward", "debugModeEnabled": "false"}
    )
    assert "'response': 'False'" in str(response.json())
    assert "'msg': 'End of debug output.'" in str(response.json())


def test_move_3():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(* x 1)"})
    response = client.post(
        "/move", json={"payload": "fastforward", "debugModeEnabled": "false"}
    )
    assert "'response': 'False'" in str(
        response.json()
    ) and "'msg': 'End of debug output.'" in str(response.json())


################################################################################
# Test: /extractterm                    ########################################
################################################################################


def test_extract_term_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(* x 1)"})
    response = client.post("/extractterm")
    assert "'response': 'True'" and "(* x 1)" in str(response.json())


def test_extract_term_2():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(/ (* a 2) 2)"})
    client.post("/addrule", json={"lhs": "(/ (* x y) z)", "rhs": "(* x (/ y z))"})
    client.post("/addrule", json={"lhs": "(* x 2)", "rhs": "(<< x 1)"})
    client.post("/addrule", json={"lhs": "(/ x x)", "rhs": "(1)"})
    client.post("/addrule", json={"lhs": "(* x 1)", "rhs": "(x)"})
    client.post("/applyrule", json={"payload": "4"})
    client.post("/applyrule", json={"payload": "6"})
    client.post("/applyrule", json={"payload": "8"})
    client.post("/applyrule", json={"payload": "10"})
    response = client.post("/extractterm")
    assert "'response': 'True'" and "a" in str(response.json())


################################################################################
# Test: /exportegraph                   ########################################
################################################################################

"""Due to the side effects of this method, you should run in manually. A png file
will be created in the current directory.
"""


@pytest.mark.skip(
    reason="Run this test manually. For more information, read comment above method <test_export_egraph_1>."
)
def test_export_egraph_1():
    client = TestClient(app)
    client.post("/createegraph", json={"payload": "(* x 1)"})
    response = client.post("/exportegraph", json={"payload": "png"})
    assert "'response': 'True'" in str(response.json())


################################################################################
# Test: /uploadsession                  ########################################
################################################################################


def test_upload_session_1():
    client = TestClient(app)
    response = client.post(
        "/uploadsession",
        json={
            "payload": '{"RewriteRules": {"0": ["0", "(* x 2)", "(<< x 1)"], "1": ["1", "(/ x x)", "(1)"]}, "Applied": ["0"], "graph": "(+ a (* a 2))", "optimalTerm": ""}'
        },
    )
    assert "'response': 'True'" in str(response.json())


def test_upload_session_2():
    client = TestClient(app)
    response = client.post(
        "/uploadsession",
        json={
            "payload": '{"RewriteRules": {"0": ["0", "(* x 2)", "(<< x 1)"], "1": ["1", "(/ x x)", "(1)"]}, "appl": ["0"], "graph": "(+ a (* a 2))"}'
        },
    )
    assert "'response': 'False'" in str(response.json())
