/**
 * This file includes all functions that are necessary for index.html and
 * egraph.html to operate properly. The following functions are available:
 *
 * - create()
 * - createEGraph()
 * - loadEGraph()
 * - exportEGraph()
 * - renderEGraph(egraph)
 * - extractBestTerm()
 * - displayExtractedBestTerm(term)
 * - createRewriteRule(lhs, rhs)
 * - displayRewriteRule(lhs, rhs, num)
 * - applyRewriteRule(number)
 * - uploadRewriteRules()
 * - downloadRewriteRules()
 * - contactServer(path, payload, httpMethod)
 * - addMessageToStatusBar(status, msg)
 * - moveThroughDebugOutput(direction)
 * - uploadSession()
 * - downloadSession()
 * - loadData()
 *
 */


/**
 * EGraphs
 *******************************************************************************
 *******************************************************************************
 *******************************************************************************
 */


/**
 * Wrapper for creating an EGraph. Makes sure user wants to delete old EGraph.
 */
function create() {
    if (String(document.getElementById("control_create_input").value) === "") {
        return;
    }
    contactServer("/loadegraph", null, "GET").then(
        function (value) {
            if (value['response'] !== "False") {
                if (confirm("There is already an EGraph. Do you want to replace it and all data attached to it?") === true) {
                    document.getElementById("rr_table").innerHTML = "";
                    addMessageToStatusBar("[INFO]", "Creating new EGraph...");
                    createEGraph();
                } else {
                    addMessageToStatusBar("[INFO]", "Action aborted.");
                }
            } else {
                createEGraph();
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.")
        });
}


/**
 * Creates an EGraph.
 */
function createEGraph() {
    contactServer("/createegraph",
        JSON.stringify({
            "payload": String(document.getElementById("control_create_input").value)
        }),
        "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
                document.getElementById("control_create_input").value = "";
            }
        }, function () {
            addMessageToStatusBar("[ERROR]", "Failed to contact server.");
        });
    loadData();
    document.getElementById("control_create_input").value = "";
}


/**
 * Loads the currently selected EGraph.
 */
function loadEGraph() {
    contactServer("/loadegraph", null, "GET").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[INFO]", value['msg']);
            } else {
                renderEGraph(value['payload2'])
                addMessageToStatusBar("[INFO]", value['msg']);
                addMessageToStatusBar("[INFO]", value['payload1'])
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.")
        });
}


/**
 * Orders server to export the current EGraph into the selected format.
 */
function exportEGraph() {
    let format;
    if (document.getElementById("export_pdf").checked) {
        format = String("pdf")
    } else if (document.getElementById("export_svg").checked) {
        format = String("svg")
    } else {
        format = String("png")
    }
    contactServer("/exportegraph",
        JSON.stringify({"payload": format}), "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * Renders an EGraph from an input string in DOT format.
 * @param {string} egraph - The EGraph in DOT format.
 */
function renderEGraph(egraph) {
    d3.select("#graph").graphviz().renderDot(egraph);
}


/**
 * Extraction of Best Term
 *******************************************************************************
 *******************************************************************************
 *******************************************************************************
 */


/**
 * Extracts best term.
 */
function extractBestTerm() {
    contactServer("/extractterm", null, "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
                displayExtractedBestTerm(value['payload']);
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * Displays the extracted term in the intended div-element.
 * @param {string} term - The extracted term
 */
function displayExtractedBestTerm(term) {
    document.getElementById("term").innerHTML = term;
}


/**
 * Rewrite Rules
 *******************************************************************************
 *******************************************************************************
 *******************************************************************************
 */


/**
 * Creates a Rewrite Rule.
 * @param {string} lhs - Left-hand side of the rewrite rule
 * @param {string} rhs - Right-hand side of the rewrite rule
 */
function createRewriteRule(lhs, rhs) {
    let left;
    let right;
    if (lhs === "" && rhs === "") {
        left = String(document.getElementById("rewrite_rule_create_left").value)
        right = String(document.getElementById("rewrite_rule_create_right").value)
    } else {
        left = String(lhs);
        right = String(rhs);
    }
    if (left === "" || right === "") {
        return;
    }
    contactServer("/addrule", JSON.stringify({
        "payload": "rule", "lhs": left, "rhs": right
    }), "POST").then(function (value) {
        if (value['response'] === "False") {
            addMessageToStatusBar("[WARN]", value['msg']);
        } else {
            addMessageToStatusBar("[INFO]", value['msg']);
            loadRewriteRules();
        }
    }, function () {
        addMessageToStatusBar("[ERROR]", "Failed to contact server.");
    });
}


/**
 * Displays a given Rewrite Rule.
 * @param {string} lhs - Left-hand side of the rewrite rule
 * @param {string} rhs - Right-hand side of the rewrite rule
 * @param {string} num - The number of the given rewrite rule.
 */
function displayRewriteRule(lhs, rhs, num) {
    const heading = document.createElement("div");
    heading.classList.add("row", "rr");
    heading.style.marginBottom = "5px";
    const a1 = document.createElement("div");
    const a2 = document.createElement("div");
    a1.classList.add("col-7");
    a2.classList.add("col-4");
    const b1 = document.createElement("b");
    const b2 = document.createElement("b");
    b1.innerHTML = lhs + " => " + rhs;
    b2.innerHTML = String(num);
    a1.appendChild(b1);
    const formDiv = document.createElement("div");
    formDiv.classList.add("form-check");
    formDiv.style.paddingLeft = "50px";
    const inputCheckbox = document.createElement("input");
    const labelForCheckbox = document.createElement("label");
    inputCheckbox.classList.add("form-check-input", "checkboxRR");
    inputCheckbox.type = "checkbox";
    inputCheckbox.value = "";
    inputCheckbox.id = "inputCheckbox" + String(num);
    labelForCheckbox.classList.add("form-check-label");
    labelForCheckbox.setAttribute("for", "inputCheckbox" + String(num));
    labelForCheckbox.appendChild(b2);
    formDiv.appendChild(inputCheckbox);
    formDiv.appendChild(labelForCheckbox);
    heading.appendChild(a1);
    heading.appendChild(a2);
    a2.appendChild(formDiv);
    document.getElementById("rr_table").appendChild(heading);
    document.getElementById("rewrite_rule_create_left").value = "";
    document.getElementById("rewrite_rule_create_right").value = "";
}


/**
 * Applies the Rewrite Rule that is registered under a certain number.
 */
function applyRewriteRules() {
    let rrNumbers = [];
    for (const element of document.getElementsByClassName("checkboxRR")) {
        if (element.checked) {
            rrNumbers.push(String(element.id).at(-1))
        }
    }
    contactServer("/applyrule",
        JSON.stringify({"payload": rrNumbers}), "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * Apply all rewrite rules till egraph is saturated.
 */
function applyAllRewriteRules() {
    contactServer("/applyallrules",
        null, "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * Load all rewrites rules.
 */
function loadRewriteRules() {
    contactServer("/getrules",
        null, "GET").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[INFO]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
                document.getElementById("rr_table").innerHTML = "";
                const data = JSON.parse(JSON.stringify(value['payload']));
                for (const item of Object.keys(data)) {
                    displayRewriteRule(data[item][1], data[item][2], data[item][0]);
                }
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * Upload rewrites rules from JSON file to server.
 */
function uploadRewriteRules() {
    let upload_input_form = document.createElement('input');
    upload_input_form.type = 'file';
    upload_input_form.onchange = _this => {
        let files = Array.from(upload_input_form.files);
        let s = Array.from(files.filter(s => (s.type === "application/json")));
        let t = s.at(0);
        let reader = new FileReader();
        reader.readAsText(t);
        reader.onload = function () {
            try {
                contactServer("/uploadrules", JSON.stringify({
                    "payload": reader.result.trim()
                }), "POST").then(function (value) {
                    if (value['response'] === "False") {
                        addMessageToStatusBar("[WARN]", value['msg']);
                    } else {
                        addMessageToStatusBar("[INFO]", value['msg']);
                        loadRewriteRules();
                    }
                }, function () {
                    addMessageToStatusBar("[ERROR]", "Failed to contact server.");
                });
            } catch (error) {
                addMessageToStatusBar("[ERROR]", "File could not be parsed.");
            }
        };
    };
    upload_input_form.click();
}


/**
 * Commands server to save all rewrites rules to JSON file.
 */
function downloadRewriteRules() {
    contactServer("/downloadrules", null, "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * General functionality
 *******************************************************************************
 *******************************************************************************
 *******************************************************************************
 */


/**
 * Contacts the server and returns the result.
 * @param {string} path - The destination path.
 * @param {string} payload - Data in JSON format.
 * @param {string} httpMethod - Either GET or POST.
 * @returns {json} Data retrieved from the server in JSON format.
 */
async function contactServer(path, payload, httpMethod) {
    let request;
    if (payload == null) {
        request = new Request("http://127.0.0.1:8000" + path, {
            method: httpMethod
        });
    } else {
        request = new Request("http://127.0.0.1:8000" + path, {
            method: httpMethod,
            body: payload,
        });
    }
    return (await fetch(request)).json();
}


/**
 * Adds a message to the status bar.
 * @param {string} status - One of the following: [INFO], [ERROR], [WARN]
 * @param {string} msg - The actual message that should be displayed.
 */
function addMessageToStatusBar(status, msg) {
    let rowDiv = document.createElement("div");
    let statusDiv = document.createElement("div");
    let msgDiv = document.createElement("div");
    rowDiv.className = "row";
    rowDiv.classList.add("msgContainer");
    rowDiv.style.margin = "5px";
    rowDiv.style.padding = "5px";
    rowDiv.style.border = "1.5px solid black";
    rowDiv.style.borderRadius = "6px";
    statusDiv.style.fontWeight = "bold";
    statusDiv.className = "col-4";
    msgDiv.style.fontWeight = "bold";
    msgDiv.style.fontFamily = "monospace";
    msgDiv.className = "col-12";
    if (status === "[ERROR]") {
        statusDiv.style.color = "#b40808";
        rowDiv.style.backgroundColor = "#e39b9b";
    } else if (status === "[INFO]") {
        statusDiv.style.color = "#077c7c";
        rowDiv.style.backgroundColor = "#9be3e3";
    } else {
        statusDiv.style.color = "#c47011";
        rowDiv.style.backgroundColor = "#ffc88e";
    }
    statusDiv.innerHTML = status;
    msgDiv.innerHTML = msg;
    msgDiv.style.paddingRight = "0px";
    rowDiv.appendChild(statusDiv);
    rowDiv.appendChild(msgDiv);
    document.getElementById("status_msg").appendChild(rowDiv);
    document.getElementById("status_msg").scrollTop =
        document.getElementById("status_msg").scrollHeight;
}


/**
 * Moves through debug output and displays the new state of the EGraph.
 * @param {string} direction - Tells the server in which direction to move
 * (forward, backward, fastforward, fastbackward).
 */
function moveThroughDebugOutput(direction) {
    contactServer("/move", JSON.stringify({
        "payload": direction,
        "debugModeEnabled": String(document.getElementById("mode_debug").checked)
    }), "POST").then(function (value) {
        if (value['response'] === "False") {
            addMessageToStatusBar("[WARN]", value['msg']);
        } else {
            addMessageToStatusBar("[INFO]", value['msg']);
            loadEGraph();
        }
    }, function () {
        addMessageToStatusBar("[ERROR]",
            "Failed to contact server.");
    });
}


/**
 * Handles the upload of a JSON file containing a session and sends it to the
 * server.
 */
function uploadSession() {
    let upload_input_form = document.createElement('input');
    upload_input_form.type = 'file';
    upload_input_form.onchange = _this => {
        let files = Array.from(upload_input_form.files);
        let s = Array.from(files.filter(s => (s.type === "application/json")));
        let t = s.at(0);
        let reader = new FileReader();
        reader.readAsText(t);
        reader.onload = function () {
            try {
                contactServer("/uploadsession", JSON.stringify({
                    "payload": reader.result.trim()
                }), "POST").then(function (value) {
                    if (value['response'] === "False") {
                        addMessageToStatusBar("[WARN]", value['msg']);
                    } else {
                        addMessageToStatusBar("[INFO]", value['msg']);
                        loadData();
                    }
                }, function () {
                    addMessageToStatusBar("[ERROR]",
                        "Failed to contact server.");
                });
            } catch (error) {
                addMessageToStatusBar("[ERROR]",
                    "File could not be parsed.");
            }
        };
    };
    upload_input_form.click();
}


/**
 * Orders the server to save the session into a JSON file.
 */
function downloadSession() {
    contactServer("/downloadsession", null, "POST").then(
        function (value) {
            if (value['response'] === "False") {
                addMessageToStatusBar("[WARN]", value['msg']);
            } else {
                addMessageToStatusBar("[INFO]", value['msg']);
            }
        }, function () {
            addMessageToStatusBar("[ERROR]",
                "Failed to contact server.");
        });
}


/**
 * Loads all the necessary data when the page is refreshed.
 */
function loadData() {
    loadEGraph();
    loadRewriteRules();
}


/**
 * Copies the extracted term to the clipboard.
 */
async function copyTextToClipboard() {
    if (String(document.getElementById("term").innerHTML).trim() !== "") {
        try {
            await navigator.clipboard.writeText(String(document.getElementById("term").innerHTML).trim());
        } catch (Error) {
            console.log("Couldn't perform copy to clipboard.");
        }
    }
}


/**
 * Expands or collapses the second or third column in the grid.
 */
function expandOrCollapseGridContainer(column) {
    if (column === '1') {
        if (document.getElementById("gridCol1").style.maxWidth !== "10%") {
            document.getElementById("gridCol1").style.maxWidth = "10%";
            document.getElementById("accordionPanelsStayOpenExample").style.display = "none";
            document.getElementById("ruleSection").style.display = "none";
            document.getElementById("buttonRR").style.display = "none";
        } else {
            document.getElementById("gridCol1").style.maxWidth = "";
            document.getElementById("accordionPanelsStayOpenExample").style.display = "";
            document.getElementById("ruleSection").style.display = "";
            document.getElementById("buttonRR").style.display = "";
        }
    } else {
        if (document.getElementById("gridCol2").style.maxWidth !== "10%") {
            document.getElementById("gridCol2").style.maxWidth = "10%";
            document.getElementById("accordion").style.display = "none";
            document.getElementById("status_div").style.display = "none";
        } else {
            document.getElementById("gridCol2").style.maxWidth = "";
            document.getElementById("accordion").style.display = "";
            document.getElementById("status_div").style.display = "";
        }
    }
}
