# -*- coding: utf-8 -*-
"""Algebra blocks module: fluent builder API for Pratt parser symbol tables."""

from dataclasses import dataclass, field, replace
from enum import IntEnum
from typing import Self


class Fixity(IntEnum):
    INFIX = 1
    PREFIX = 2
    POSTFIX = 3
    MATCHFIX = 4
    NOFIX = 5


class Assoc(IntEnum):
    LEFT = 1
    RIGHT = 2
    NONE = 3


@dataclass(frozen=True)
class Symbol:
    """A symbol registered in an algebra block."""

    literal: str
    name: str
    binding_power: int = 0
    fixity: Fixity | None = None
    assoc: Assoc | None = None
    close: str | None = None
    is_commutative: bool = False
    is_associative: bool = False
    is_idempotent: bool = False
    is_involutive: bool = False
    is_short_circuit: bool = False
    identity_token: str | None = None
    annihilator_token: str | None = None

    def bp(self, n: int) -> Self:
        if n <= 0:
            raise ValueError("Binding power must be a positive integer.")
        return replace(self, binding_power=n)

    def left(self) -> Self:
        return replace(self, assoc=Assoc.LEFT)

    def right(self) -> Self:
        return replace(self, assoc=Assoc.RIGHT)

    def noassoc(self) -> Self:
        return replace(self, assoc=Assoc.NONE)

    def infix(self) -> Self:
        return replace(self, fixity=Fixity.INFIX)

    def prefix(self) -> Self:
        if self.assoc is not None:
            raise ValueError("Prefix symbols must not specify associativity.")
        return replace(self, fixity=Fixity.PREFIX)

    def postfix(self) -> Self:
        if self.assoc is not None:
            raise ValueError("Postfix symbols must not specify associativity.")
        return replace(self, fixity=Fixity.POSTFIX)

    def matchfix(self, close: str) -> Self:
        if self.assoc is not None:
            raise ValueError("Matchfix symbols must not specify associativity.")
        return replace(self, fixity=Fixity.MATCHFIX, close=close)

    def nofix(self) -> Self:
        return replace(self, fixity=Fixity.NOFIX)

    def constant(self) -> Self:
        return replace(self, fixity=Fixity.NOFIX)

    def commutative(self) -> Self:
        return replace(self, is_commutative=True)

    def associative(self) -> Self:
        return replace(self, is_associative=True)

    def idempotent(self) -> Self:
        return replace(self, is_idempotent=True)

    def involutive(self) -> Self:
        return replace(self, is_involutive=True)

    def shortCircuit(self) -> Self:
        return replace(self, is_short_circuit=True)

    def identity(self, e: str) -> Self:
        return replace(self, identity_token=e)

    def annihilator(self, z: str) -> Self:
        return replace(self, annihilator_token=z)


@dataclass(frozen=True)
class RewriteRule:
    """A named algebraic identity (lhs, rhs) in an algebra's notation."""

    name: str
    lhs: str
    rhs: str


@dataclass(frozen=True)
class AlgebraBlock:
    """A named collection of symbols and rewrite rules for one notational system."""

    name: str
    _symbols: tuple[Symbol, ...] = field(default_factory=tuple)
    _rules: tuple[RewriteRule, ...] = field(default_factory=tuple)

    def add(self, item: Symbol | RewriteRule) -> Self:
        match item:
            case Symbol():
                return replace(self, _symbols=self._symbols + (item,))
            case RewriteRule():
                return replace(self, _rules=self._rules + (item,))

    def lookup(self, literal: str) -> list[Symbol]:
        return [s for s in self._symbols if s.literal == literal]
