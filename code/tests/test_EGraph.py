"""This file contains tests to ensure the capability and correctness of EGraph.py
The tests are separated into groups to test different aspects of EGraph.py.

- Number of Tests: 25

"""

import os
import pytest
import AbstractSyntaxTree
import EGraph
import RewriteRule


################################################################################
# General functionality                 ########################################
################################################################################


def test_egraph_general_1():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    assert len(egraph.u.subsets()) == 4


def test_egraph_general_2():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    g = EGraph.EGraph()
    etermid = g.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))"),
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, etermid, g)
    assert len(egraph.u.subsets()) == 4
    assert len(egraph.h.keys()) == 8


def test_egraph_general_3():
    ast = AbstractSyntaxTree.AbstractSyntaxTree(
        "(* (>> (<< 1 (- a 4)) c) (/ (* (+ 2 3) (- 3 4)) 4))"
    )
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    assert len(egraph.h.keys()) == 14


def test_egraph_general_4():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    enode_keys = [enode.key for enode in egraph.h.keys()]
    assert "/" in enode_keys
    assert "*" in enode_keys
    assert "a" in enode_keys
    assert "2" in enode_keys


def test_egraph_general_5():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    ast2 = AbstractSyntaxTree.AbstractSyntaxTree("(* a 2)")
    ast3 = AbstractSyntaxTree.AbstractSyntaxTree("(<< a 1)")
    g = EGraph.EGraph()
    g.add_node(ast.root_node)
    id1 = g.add_node(ast2.root_node)
    id2 = g.add_node(ast3.root_node)
    g.merge(id1, id2)
    g.rebuild()
    assert g._find(id1) == g._find(id2)


def test_egraph_general_6():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ z (* w (/ x y)))")
    ast2 = AbstractSyntaxTree.AbstractSyntaxTree("(* w (/ x y))")
    ast3 = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* w x)) y")
    g = EGraph.EGraph()
    g.add_node(ast.root_node)
    id1 = g.add_node(ast2.root_node)
    id2 = g.add_node(ast3.root_node)
    g.merge(id1, id2)
    g.rebuild()
    assert g._find(id1) == g._find(id2)


def test_egraph_general_7():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ a 2)")
    g = EGraph.EGraph()
    g.add_node(ast.root_node)
    eclasses = g.get_eclasses()
    rule = RewriteRule.RewriteRule("switch", "(+ x y)", "(+ y x)")
    list_of_matches = g._ematch(eclasses, rule.expr_lhs.root_node)
    eclass_id, environment = list_of_matches[0]
    new_eclass_id = g._substitute(rule.expr_rhs.root_node, environment)
    assert g._find(new_eclass_id)


def test_egraph_general_8():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* a (/ a a))")
    g = EGraph.EGraph()
    etermid = g.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, etermid, g)
    assert best == "a"


################################################################################
# Extract                               ########################################
################################################################################


def test_extraction_1():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    g = EGraph.EGraph()
    etermid = g.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))"),
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, etermid, g)
    assert best == "a"


def test_extraction_2():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* a 1)")
    g = EGraph.EGraph()
    etermid = g.add_node(ast.root_node)
    rules = [RewriteRule.RewriteRule("simp", "(* x 1)", "(x)")]
    egraph, dbg, best = EGraph.equality_saturation(rules, etermid, g)
    assert best == "a"


def test_extraction_3():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* a 2)")
    g = EGraph.EGraph()
    etermid = g.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))"),
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, etermid, g)
    assert best == "(<< a 1)"


def test_extraction_4():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* 0 (* (+ a (* a 2)) 1))")
    egraph = EGraph.EGraph()
    eterm_id = egraph.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
        RewriteRule.RewriteRule("zero", "(* 0 x)", "(0)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    assert best == "0"


def test_extraction_5():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* a 2)")
    egraph = EGraph.EGraph()
    eterm_id = egraph.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))"),
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    _, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    egraph, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    assert best == "(<< a 1)"


def test_extraction_6():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ a 2)")
    g = EGraph.EGraph()
    etermid = g.add_node(ast.root_node)
    assert "(+ a 2)" == EGraph._extract_term(etermid, g)


################################################################################
# E-Matching                            ########################################
################################################################################


def test_e_matching_1():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ a 1)")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    rules = [RewriteRule.RewriteRule("simp", "(* x 3)", "(* 1 x)")]
    matches = egraph._ematch(egraph.get_eclasses(), rules[0].expr_lhs.root_node)
    assert matches == []


def test_e_matching_2():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* (/ (- a 3) a)(* 2 b))")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    rules = [RewriteRule.RewriteRule("mul", "(* x y)", "(* y x)")]
    matches = egraph._ematch(egraph.get_eclasses(), rules[0].expr_lhs.root_node)
    assert len(matches) == 2


def test_e_matching_3():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    eclasses = egraph.get_eclasses()
    r = RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))")
    list_of_matches = egraph._ematch(eclasses, r.expr_lhs.root_node)
    assert (
        "x" in list_of_matches[0][1].keys()
        and "y" in list_of_matches[0][1].keys()
        and "z" in list_of_matches[0][1].keys()
    )


def test_e_matching_4():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ a 2)")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    eclasses = egraph.get_eclasses()
    r = RewriteRule.RewriteRule("switch", "(+ x y)", "(+ y x)")
    list_of_matches = egraph._ematch(eclasses, r.expr_lhs.root_node)
    assert "x" in list_of_matches[0][1].keys() and "y" in list_of_matches[0][1].keys()


def test_e_matching_5():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(<< a (* b 2))")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    eclasses = egraph.get_eclasses()
    r = RewriteRule.RewriteRule("reassociate", "(* x 2)", "(<< x 1)")
    enodes = [enode for enode in egraph.h.keys()]
    enode_b = None
    for enode in enodes:
        if enode.key == "b":
            enode_b = enode
    list_of_matches = egraph._ematch(eclasses, r.expr_lhs.root_node)
    assert str(egraph.h[enode_b]) in list_of_matches[0][1].values()


################################################################################
# EGraph in DOT format                  ########################################
################################################################################

"""The method ``egraph_to_dot`` is extremely well tested, not by unit tests but
manually. Extreme efforts were made to ensure it works as expected. If you still
would like to see some results, you can run the tests under this comment. They
will create pdfs of the egraphs in the current directory.
"""


@pytest.mark.skip(
    reason="Run this test manually. For more information, read comment above method <test_egraph_to_dot_1>."
)
def test_egraph_to_dot_1():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    egraph = EGraph.EGraph()
    eterm_id = egraph.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))"),
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    EGraph.export_egraph_to_file(egraph.egraph_to_dot(), str(os.getcwd()))
    assert True


@pytest.mark.skip(
    reason="Run this test manually. For more information, read comment above method <test_egraph_to_dot_1>."
)
def test_egraph_to_dot_2():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* (>> b 2) (/ c 3))")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    EGraph.export_egraph_to_file(egraph.egraph_to_dot(), str(os.getcwd()))
    assert True


@pytest.mark.skip(
    reason="Run this test manually. For more information, read comment above method <test_egraph_to_dot_1>."
)
def test_egraph_to_dot_3():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* (/ (- a 3) a)(* 2 b))")
    egraph = EGraph.EGraph()
    egraph.add_node(ast.root_node)
    EGraph.export_egraph_to_file(egraph.egraph_to_dot(), str(os.getcwd()))
    assert True


@pytest.mark.skip(
    reason="Run this test manually. For more information, read comment above method <test_egraph_to_dot_1>."
)
def test_egraph_to_dot_4():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* 0 (* (+ a (* a 2)) 1))")
    egraph = EGraph.EGraph()
    eterm_id = egraph.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
        RewriteRule.RewriteRule("zero", "(* 0 x)", "(0)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    EGraph.export_egraph_to_file(egraph.egraph_to_dot(), str(os.getcwd()))
    assert True


################################################################################
# Edge case                             ########################################
################################################################################


def test_edge_case_1():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(a)")
    egraph = EGraph.EGraph()
    eterm_id = egraph.add_node(ast.root_node)
    rules = [RewriteRule.RewriteRule("expand", "(x)", "(* x 1)")]
    egraph, debug_output = EGraph.apply_rules(rules, egraph)
    egraph, debug_output = EGraph.apply_rules(rules, egraph)
    assert len(egraph.u.subsets()) == 2
    assert "a" == EGraph._extract_term(eterm_id, egraph)


def test_edge_case_2():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    egraph = EGraph.EGraph()
    eterm_id = egraph.add_node(ast.root_node)
    rules = [
        RewriteRule.RewriteRule("reassociate", "(/ (* x y) z)", "(* x (/ y z))"),
        RewriteRule.RewriteRule("shift", "(* x 2)", "(<< x 1)"),
        RewriteRule.RewriteRule("simplify", "(/ x x)", "(1)"),
        RewriteRule.RewriteRule("simp", "(* x 1)", "(x)"),
        RewriteRule.RewriteRule(
            "reassociate_reverse", "(* x (/ y z))", "(/ (* x y) z)"
        ),
        RewriteRule.RewriteRule("shift_reverse", "(<< x 1)", "(* x 2)"),
        RewriteRule.RewriteRule("simplify_reverse", "(1)", "(/ x x)"),
        RewriteRule.RewriteRule("simp_reverse", "(x)", "(* x 1)"),
    ]
    egraph, dbg, best = EGraph.equality_saturation(rules, eterm_id, egraph)
    assert best == "a"
