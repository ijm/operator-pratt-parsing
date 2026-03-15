# -*- coding: utf-8 -*-
"""Structural algebra block: foundational grouping and list-construction symbols."""

from algebra_block import AlgebraBlock, Symbol

block: AlgebraBlock = (
    AlgebraBlock("structural")
    .add(Symbol("(", "lparen").matchfix(")"))
    .add(Symbol(",", "comma").infix().bp(2).right().associative())
    .add(Symbol(";", "semicolon").infix().bp(1).right().associative())
    .add(Symbol("[", "apply").matchfix("]").bp(95))
)
