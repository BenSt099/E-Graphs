"""This file contains tests to ensure the capability and correctness of
AbstractSyntaxTree.py and AbstractSyntaxTreeNode.py

- Number of Tests: 20

"""

import AbstractSyntaxTree


def test_ast_1():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* a 2) 2)")
    assert "(/ (* a 2) 2)" == str(ast)


def test_ast_2():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ a (* a 2) )")
    assert "(+ a (* a 2))" == str(ast)


def test_ast_3():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(- a (<< a 2))")
    assert "(- a (<< a 2))" == str(ast)


def test_ast_4():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(+ a b)")
    assert "(+ a b)" == str(ast)


def test_ast_5():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* (>> b 2) (/ c 3))")
    assert "(* (>> b 2) (/ c 3))" == str(ast)


def test_ast_6():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(<< a (* 2 b))")
    assert "(<< a (* 2 b))" == str(ast)


def test_ast_7():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* (/ (- a 3) a)(* 2 b))")
    assert "(* (/ (- a 3) a) (* 2 b))" == str(ast)


def test_ast_8():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ x x)")
    assert "(/ x x)" == str(ast)


def test_ast_9():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(x)")
    assert "(x)" == str(ast)


def test_ast_10():
    ast = AbstractSyntaxTree.AbstractSyntaxTree(
        "(* (>> (<< 1 (- a 4)) c) (/ (* (+ 2 3) (- 3 4)) 4))"
    )
    assert "(* (>> (<< 1 (- a 4)) c) (/ (* (+ 2 3) (- 3 4)) 4))" == str(ast)


def test_ast_11():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (* var 23) 2)")
    assert "(/ (* var 23) 2)" == str(ast)


def test_ast_12():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(/ (<< var 23) 2)")
    assert "(/ (<< var 23) 2)" == str(ast)


def test_ast_13():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(var)")
    assert "(var)" == str(ast)


def test_ast_14():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* ( +  1 a ) x  )")
    assert "(* (+ 1 a) x)" == str(ast)


def test_ast_15():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(* ( <<  1 a ) x  )")
    assert "(* (<< 1 a) x)" == str(ast)


def test_ast_16():
    ast = AbstractSyntaxTree.AbstractSyntaxTree(" ( >> a9 ( / ip 7) )")
    assert "(>> a9 (/ ip 7))" == str(ast)


def test_ast_17():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("( vv )")
    assert "(vv)" == str(ast)


def test_ast_18():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("( / (>> x 9999 ) vai9)")
    assert "(/ (>> x 9999) vai9)" == str(ast)


def test_ast_19():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(   23 )")
    assert "(23)" == str(ast)


def test_ast_20():
    ast = AbstractSyntaxTree.AbstractSyntaxTree("(- xx (* a yy_y))")
    assert "(- xx (* a yy_y))" == str(ast)
