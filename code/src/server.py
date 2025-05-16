"""This file implements a FastAPI server.

Paths:
    - ``/getrules``: GET
    - ``/addrule``: POST
    - ``/applyrule``: POST
    - ``/applyallrules``: POST
    - ``/downloadrules``: POST
    - ``/uploadrules``: POST
    - ``/createegraph``: POST
    - ``/loadegraph``: GET
    - ``/move``: POST
    - ``/extractterm``: POST
    - ``/exportegraph``: POST
    - ``/downloadsession``: POST
    - ``/uploadsession``: POST

Documentation:
    The API documentation is available at: ``http://127.0.0.1:8000/dokumentation.html``

FastAPI:
    FastAPI is used as Backend Server (url: https://fastapi.tiangolo.com/)
"""

from contextlib import asynccontextmanager
from json import JSONDecodeError
from os.path import realpath
from webbrowser import open_new

from fastapi import FastAPI
from fastapi import Request
from starlette.staticfiles import StaticFiles

from EGraphService import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """This function is needed for FastAPI to open a browser tab with the
    corresponding address. It is executed before anything else.
    """
    open_new(r"http://127.0.0.1:8000")
    yield


app = FastAPI(lifespan=lifespan)
egraphService = EGraphService()


@app.get("/getrules")
def get_rules():
    """Collects all rewrite rules from the service and returns them.

    :return: JSON, {'response': ..., 'msg': ..., 'payload': ...}
    """
    result, msg, data = egraphService.get_all_rules()
    return {"response": str(result), "msg": msg, "payload": data}


@app.post("/addrule")
async def add_rule(request: Request):
    """Takes a new rewrite rule and adds it to the service.

    :param request: JSON, {"payload": "rule", "lhs": ..., "rhs": ...}
    :return: JSON, {'response': ..., 'msg': ..., 'payload': ...}
    """
    payload = await request.body()
    json_data = json.loads(payload)
    result, msg = egraphService.add_rule(json_data["lhs"], json_data["rhs"])
    return {"response": str(result), "msg": msg}


@app.post("/applyrule")
async def apply_rule(request: Request):
    """Applies rewrite rule(s) to egraph.

    :param request: JSON, {'payload': ...}
    :return: JSON, {'response': ..., 'msg': ...}
    """
    payload = await request.body()
    json_data = json.loads(payload)
    result, msg = egraphService.apply(json_data["payload"])
    return {"response": str(result), "msg": msg}


@app.post("/applyallrules")
async def apply_all_rules():
    """Apply all rules

    :return: JSON, {'response': ..., 'msg': ...}
    """
    result, msg = egraphService.apply_all_rules()
    return {"response": str(result), "msg": msg}


@app.post("/downloadrules")
async def download_rules():
    """Saves all rewrite rules from the service in a JSON file.

    :return: JSON, {"response": ..., "msg": ...}
    """
    result, msg = egraphService.save_rewrite_rules_to_file()
    return {"response": str(result), "msg": msg}


@app.post("/uploadrules")
async def upload_rules(request: Request):
    """Adds all rewrite rules from the uploaded JSON file to the service.

    :param request: JSON, {'payload': ...}
    :return: JSON, {'response': ..., 'msg': ...}
    """
    payload = await request.body()
    try:
        json_data = json.loads(payload)
    except JSONDecodeError:
        return {"response": "False", "msg": "Failed to decode JSON."}
    result, msg = egraphService.add_rewrite_rules_from_file(
        json.loads(json_data["payload"])
    )
    return {"response": str(result), "msg": msg}


@app.post("/createegraph")
async def create_egraph(request: Request):
    """Creates a new E-Graph and adds two default rewrite rules.

    :param request: JSON, {'payload': ...}
    :return: JSON, {"response": ..., "msg": ...}
    """
    payload = await request.body()
    json_data = json.loads(payload)
    result, msg = egraphService.create_egraph(json_data["payload"])
    egraphService.add_rule("(* x 2)", "(<< x 1)")
    egraphService.add_rule("(/ x x)", "(1)")
    return {"response": str(result), "msg": msg}


@app.get("/loadegraph")
def load_egraph():
    """Returns the currently selected E-Graph in DOT format.

    :return: JSON, {'response': ..., 'msg': ..., 'payload1': ..., 'payload2': ...}
    """
    result, msg, data = egraphService.get_current_egraph()
    return {
        "response": str(result),
        "msg": msg,
        "payload1": data[0],
        "payload2": data[1],
    }


@app.post("/move")
async def move(request: Request):
    """Steps forward/backward/fastforward/fastbackward in debug information.

    :param request: JSON, {'payload': ..., 'debugModeEnabled': ...}
    :return: JSON, {response: ..., 'msg': ...}
    """
    payload = await request.body()
    json_data = json.loads(payload)
    if json_data["payload"] == "backward" and json_data["debugModeEnabled"] == "false":
        return {
            "response": "False",
            "msg": "Could NOT load debug output. Use debug (>) output to watch extraction.",
        }
    elif (
        json_data["payload"] == "backward" and json_data["debugModeEnabled"] != "false"
    ):
        if egraphService.current_minor == 0:
            if egraphService.current_major == 0:
                return {"response": "False", "msg": "End of debug output."}
        egraphService.move_backward()
    elif json_data["payload"] == "forward" and json_data["debugModeEnabled"] == "false":
        return {
            "response": "False",
            "msg": "Could NOT load debug output. Use debug (>) output to watch extraction.",
        }
    elif json_data["payload"] == "forward" and json_data["debugModeEnabled"] != "false":
        if (
            len(egraphService.egraphs[egraphService.current_major]) - 1
            == egraphService.current_minor
        ):
            if egraphService.current_major == len(egraphService.egraphs) - 1:
                return {"response": "False", "msg": "End of debug output."}
        egraphService.move_forward()
    elif json_data["payload"] == "fastbackward":
        if egraphService.current_major != 0:
            egraphService.move_fastbackward()
        else:
            return {"response": "False", "msg": "Start of debug output."}
    elif json_data["payload"] == "fastforward":
        if egraphService.current_major != len(egraphService.egraphs) - 1:
            egraphService.move_fastforward()
        else:
            return {"response": "False", "msg": "End of debug output."}
    else:
        return {"response": "False", "msg": "Failed to move."}
    return {"response": "True", "msg": json_data["payload"] + "."}


@app.post("/extractterm")
async def extract_term():
    """Extracts best term from E-Graph and returns it.

    :return: JSON, {"response": ..., "msg": ..., 'payload': ...}
    """
    result, msg, data = egraphService.extract()
    return {"response": str(result), "msg": msg, "payload": data}


@app.post("/exportegraph")
async def export_egraph(request: Request):
    """Exports current E-Graph into one format.

    :param request: JSON, {'payload': ...}
    :return: JSON, {"response": ..., "msg": ...}
    """
    payload = await request.body()
    json_data = json.loads(payload)
    result, msg = egraphService.export(json_data["payload"])
    return {"response": str(result), "msg": msg}


@app.post("/downloadsession")
async def download_session():
    """Saves the current session to a file.

    :return: JSON, {"response": ..., "msg": ...}
    """
    result, msg = egraphService.save_session_to_file()
    return {"response": str(result), "msg": msg}


@app.post("/uploadsession")
async def upload_session(request: Request):
    """Processes the uploaded session file.

    :param request: JSON, {'payload': ...}
    :return: JSON, {"response": ..., "msg": ..., 'payload': ...}
    """
    payload = await request.body()
    json_data = json.loads(payload)
    result, msg = egraphService.set_session_from_file(json.loads(json_data["payload"]))
    return {"response": str(result), "msg": msg}


"""
This last line enables the app to access all content in the static/ folder.
Due to issues with testing the above methods, a fix was applied. For more
information, please visit: https://github.com/fastapi/fastapi/issues/3550
"""
app.mount(
    "/",
    StaticFiles(directory=realpath(f"{realpath(__file__)}/../static"), html=True),
    name="static",
)
