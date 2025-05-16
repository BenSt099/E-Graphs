"""This module contains the EGraphService and a function to check expressions.

Classes:
    EGraphService

    Methods:
        - create_egraph(expr)
        - get_current_egraph()
        - extract()
        - export(extension_format)
        - get_all_rules()
        - add_rule(lhs, rhs)
        - apply_all_rules_randomly()
        - apply(rules)
        - save_rewrite_rules_to_file()
        - add_rewrite_rules_from_file(data)
        - get_snapshot()
        - save_session_to_file()
        - set_session_from_file(data)
        - move_backward()
        - move_forward()
        - move_fastbackward()
        - move_fastforward()

Functions:
    is_valid_expression
"""

import os
import json
from datetime import datetime
from EGraph import (
    EGraph,
    apply_rules,
    export_egraph_to_file,
    equality_saturation,
    equality_saturation_no_extract, _extract_term,
)
from RewriteRule import RewriteRule
from AbstractSyntaxTree import AbstractSyntaxTree


def is_valid_expression(expression):
    """This function checks if the given expression is a valid expression.
    This is done by trying to create an AST. If it works, the expression could
    still be invalid. Therefore, the string representation is compared to the
    original expression.

    :param expression: A string in prefix-notation
    :return: Returns True if the expression is valid, False otherwise.
    """
    expression = expression.strip()
    try:
        ast = AbstractSyntaxTree(expression)
    except IndexError:
        return False

    return (
        expression == str(ast)
        and expression.startswith("(")
        and expression.endswith(")")
    )


class EGraphService:
    """Class that represents the EGraphService.

    Attributes:
        - rrc: rewrite rule counter
        - dict_of_rules: Dictionary of rules
        - applied_rules: List of applied rules
        - egraph: current E-Graph
        - expr: The expression to the corresponding E-Graph
        - egraphs: List with debug strings
        - current_major: pointer
        - current_minor: pointer
    """

    def __init__(self):
        """Initialises class. Takes no arguments.

        :returns: None.
        """
        self.rrc = 0
        self.dict_of_rules = {}
        self.applied_rules = set()
        self.egraph = None
        self.expr = None
        self.egraphs = [[]]
        self.current_major = 0
        self.current_minor = 0

    def create_egraph(self, expression):
        """Creates an e-graph thereby clearing all previously made settings.

        :param expression: mathematical expression, prefix notation
        :return: Boolean, str (if action is successful, status msg)
        """
        if not is_valid_expression(expression):
            return False, "Invalid expression."
        eg = EGraph()
        eterm_id = eg.add_node(AbstractSyntaxTree(expression).root_node)
        self.egraph = (eg, eterm_id)
        self.expr = expression
        self.egraphs = [[]]
        self.current_major = 0
        self.current_minor = 0
        self.egraphs[self.current_major].append(["EGraph created.", eg.egraph_to_dot()])
        self.rrc = 0
        self.dict_of_rules = {}
        return True, "Created EGraph."

    def get_current_egraph(self):
        """Returns the egraph that is currently selected by the minor and
        major pointers.

        :return: String representation of the E-Graph in DOT format.
        """
        if self.egraphs == [[]]:
            return False, "No EGraph there.", (None, None)
        else:
            return (
                True,
                "EGraph loaded.",
                self.egraphs[self.current_major][self.current_minor],
            )

    def extract(self):
        """Performs equality saturation and extracts best term.

        :return: bool, str, str (if action is successful, status msg, best term)
        """
        egraph, debug_information, best_term = equality_saturation(
            list(self.dict_of_rules.values()), self.egraph[1], self.egraph[0]
        )
        self.egraphs.append(debug_information)
        self.egraph = (egraph, self.egraph[1])

        return (
            True,
            "Extracted best term. Use debug (>) output to watch extraction.",
            best_term,
        )

    def export(self, extension_format):
        """Saves the currently selected E-Graph into a chosen format.

        :param extension_format: Determines which format should be used (pdf, svg, png).
        :return: True if successful, False otherwise.
        """
        return export_egraph_to_file(
            self.get_current_egraph()[2][1], str(os.getcwd()), extension=extension_format
        )

    def get_all_rules(self):
        """Returns all rules in dictionary format.

        :return: dictionary with rewrite rules
        """
        rules = dict()
        if self.dict_of_rules == dict():
            return False, "No rules to extract.", None
        for number, rule in self.dict_of_rules.items():
            rules[number] = [rule.name, str(rule.expr_lhs), str(rule.expr_rhs)]
        return True, "Loaded rules.", rules

    def add_rule(self, lhs, rhs):
        """Checks if rewrite rule has correct format and adds it to the service.

        :param lhs: str, left-hand side of rewrite rule
        :param rhs: str, right-hand side of rewrite rule
        :return: bool, str, str (if action is successful, status msg, number of rule)
        """
        if (
            is_valid_expression(lhs)
            and is_valid_expression(rhs)
            and lhs + " => " + rhs
            not in [
                str(rule.expr_lhs) + " => " + str(rule.expr_rhs)
                for rule in self.dict_of_rules.values()
            ]
        ):
            self.dict_of_rules[self.rrc] = RewriteRule(str(self.rrc), lhs, rhs)
            self.rrc += 1

            if rhs + " => " + lhs not in [
                str(rule.expr_lhs) + " => " + str(rule.expr_rhs)
                for rule in self.dict_of_rules.values()
            ]:
                self.dict_of_rules[self.rrc] = RewriteRule(str(self.rrc), rhs, lhs)
                self.rrc += 1
            return True, "Added rules."
        return False, "No valid rule OR Exists already."

    def apply_all_rules(self):
        """Apply all rewrite rules to the E-Graph.

        :return: bool, str (if action is successful, status msg)
        """
        egraph, debug_information = equality_saturation_no_extract(
            list(self.dict_of_rules.values()), self.egraph[1], self.egraph[0]
        )
        self.egraphs.append(debug_information)
        self.egraph = (egraph, self.egraph[1])
        return True, "Applied all rules - graph saturated."

    def apply(self, rules):
        """Apply rewrite rule(s) to the E-Graph.

        :param rules: list with rewrite rules
        :return: bool, str (if action is successful, status msg)
        """
        applied_rules_str = "Applied rule(s): "
        applied_rules = []
        for rule in rules:
            if int(rule) in self.dict_of_rules.keys():
                applied_rules.append(self.dict_of_rules[int(rule)])
                applied_rules_str += str(rule) + ", "
        applied_rules_str = applied_rules_str.strip()
        if applied_rules_str[-1] == ",":
            applied_rules_str = applied_rules_str[0 : len(applied_rules_str) - 1]
        if applied_rules:
            egraph, debug_information = apply_rules(applied_rules, self.egraph[0])
            for rule in applied_rules:
                self.applied_rules.add(rule.name)
            self.egraph = (egraph, self.egraph[1])
            self.egraphs.append(debug_information)
        else:
            return False, "No rules applied."
        return True, applied_rules_str

    def save_rewrite_rules_to_file(self):
        """Saves all rewrite rules in a JSON file.

        :return: True if successful, False otherwise.
        """
        rules = dict()
        if self.dict_of_rules == dict():
            return False, "No rules to save."
        for number, rule in self.dict_of_rules.items():
            rules[number] = [rule.name, str(rule.expr_lhs), str(rule.expr_rhs)]
        try:
            with open(
                ("rules-" + datetime.now().isoformat() + ".json").replace(":", "_"),
                mode="w",
                encoding="utf-8",
            ) as file:
                json.dump({"RewriteRules": rules}, file)
        except OSError:
            return False, "Couldn't save file, OSError."
        path = str(os.getcwd())
        return (
            True,
            "Downloaded rules in "
            + path[0 : int(len(path) / 2)]
            + " "
            + path[int(len(path) / 2) + 1 : len(path)]
            + ".",
        )

    def add_rewrite_rules_from_file(self, data):
        """Adds all rewrite rules from a file to the service.

        :param data: JSON, {'RewriteRules': ...}
        :return: bool, str (if action is successful, status msg)
        """
        try:
            rules = data["RewriteRules"]
        except KeyError:
            return False, "Format is broken."

        if len(rules.items()) < 1:
            return False, "No rewrite rules found."

        for _, rule in rules.items():
            if is_valid_expression(rule[1]) and is_valid_expression(rule[2]):
                self.add_rule(rule[1], rule[2])

        return True, "Added rewrite rules."

    def get_snapshot(self):
        """Returns a snapshot of the service in JSON format.

        :return: JSON, {'RewriteRules': ..., 'Applied': ..., 'graph': ...}
        """
        rules = dict()
        for number, rule in self.dict_of_rules.items():
            rules[number] = [rule.name, str(rule.expr_lhs), str(rule.expr_rhs)]
        best_term = _extract_term(self.egraph[1], self.egraph[0])
        return {
            "RewriteRules": rules,
            "Applied": list(self.applied_rules),
            "graph": self.expr,
            "optimalTerm": best_term,
        }

    def save_session_to_file(self):
        """Saves session in file.

        :return: bool, str (if action is successful, status msg)
        """
        try:
            with open(
                ("session-" + datetime.now().isoformat() + ".json").replace(":", "_"),
                mode="w",
                encoding="utf-8",
            ) as file:
                json.dump(self.get_snapshot(), file)
        except OSError:
            return False, "Couldn't save file, OSError."
        path = str(os.getcwd())
        return (
            True,
            "Downloaded session in "
            + path[0 : int(len(path) / 2)]
            + " "
            + path[int(len(path) / 2) + 1 : len(path)]
            + ".",
        )

    def set_session_from_file(self, data):
        """Sets service from data in session file.

        :param data: JSON, {'RewriteRules': ..., 'Applied': ..., 'graph': ...}
        :return: bool, str, str (if action is successful, status msg,
        previously applied rules)
        """
        try:
            egraph = data["graph"]
            rules = data["RewriteRules"]
            applied_rules = data["Applied"]
            optimal_term = data["optimalTerm"]
        except KeyError:
            return False, "Format is broken."
        self.create_egraph(egraph)
        self.rrc = 0
        applied_rules_str = []
        for _, rule in rules.items():
            _, number = self.add_rule(rule[1], rule[2])
            if rule[0] in applied_rules:
                applied_rules_str.append(number)
        return (
            True,
            "Uploaded session. Applied rules in last session: "
            + str(applied_rules_str)
            + " | optimal term in last session: "
            + optimal_term,
        )

    def move_backward(self):
        """Moves backward in debug output."""
        if self.current_minor == 0:
            if self.current_major == 0:
                pass
            else:
                self.current_major -= 1
                self.current_minor = len(self.egraphs[self.current_major]) - 1
        else:
            self.current_minor -= 1

    def move_forward(self):
        """Moves forward in debug output."""
        if len(self.egraphs[self.current_major]) - 1 == self.current_minor:
            if self.current_major == len(self.egraphs) - 1:
                pass
            else:
                self.current_minor = 0
                self.current_major += 1
        else:
            self.current_minor += 1

    def move_fastbackward(self):
        """Moves fastforward in debug output."""
        if self.current_major != 0:
            self.current_major -= 1
            self.current_minor = len(self.egraphs[self.current_major]) - 1

    def move_fastforward(self):
        """Moves fastbackward in debug output."""
        if self.current_major != len(self.egraphs) - 1:
            self.current_major += 1
            self.current_minor = len(self.egraphs[self.current_major]) - 1
