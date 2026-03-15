<!-- markdownlint-disable MD041 -->
## algebra-blocks.spec: Algebra Block Code File Specification

### Summary

This document defines constraints on code files that implement algebra blocks for a Pratt parser symbol table. An algebra block code file registers symbols, constants, and rewrite rules for one coherent notational system using a Fluent Builder API.

### Imports & Inheritance

This document inherits from:

* [TECHDOC Specification](techdoc.spec.md)
* [Standard Vocabulary](std.vocab.md)

This document conforms to:

* [Specification Specification](specification.spec.md)

### Terminology and Conventions

* (D01) An ALGEBRA-BLOCK is a named collection of SYMBOLS, and REWRITE-RULES belonging to one coherent notational system.
* (D02) A SYMBOL is a string literal registered in an algebra block that carries attributes like binding power, fixity, and associativity.
* (D03) A "binding power" is a positive integer encoding operator precedence; higher values bind more tightly. A value of zero is equivalent to None.
* (D04) A REWRITE-RULE is a named pair of expressions (lhs, rhs) expressed in the algebra's own notation, representing an algebraic identity applicable to the concrete syntax tree.
* (D05) A CONSTANT is a string literal registered that is not intended to be parsed as an operator.
* (D06) A Fluent Builder is a method-chaining API in which each method call returns the object under construction, allowing attributes to be appended in sequence on one logical line.

### Functional Constraints

* (FLU1) ALGEBRA-BLOCKS and SYMBOLS MUST be constructed using the Fluent Builder pattern Ⓟ
* (FLU2) ALGEBRA-BLOCKS MUST support a lookup method that returns all SYMBOL objects for a given string literal. Ⓟ
* (SYM2) A SYMBOL MAY have a binding power, a fixity, or an associativity Ⓝ
* (SYM3) A SYMBOL MAY have zero or more boolean flags indicating special properties from `commutative`, `associative`, `idempotent`, `involutive`, `shortCircuit` Ⓝ
* (SYM4) A SYMBOL MAY be associated with an identity or annihilator token Ⓝ
* (SYM5) A SYMBOL whose FIXITY is `prefix` or `postfix` MUST NOT specify an associativity. Ⓟ
* (SYM6) A SYMBOL whose FIXITY is `matchfix` MUST specify the closing glyph and MUST NOT specify an associativity. Ⓟ
* (SYM7) The same string MAY be registered as a SYMBOL more than once within one ALGEBRA-BLOCK if and only if the registrations have distinct FIXITY values. Ⓝ
* (FIX1) Fixity MUST BE one of: `infix`, `prefix`, `postfix`, `matchfix`, or None. Ⓟ
* (ACC1) Associativity MUST BE one of: `left`, `right`, or `none`. Ⓟ
* (BP1) BINDING-POWER values MUST be positive integers. Ⓟ
* (BP2) BINDING-POWER values SHOULD be assigned from the ranges defined in the reference range table below. Ⓗ
* (CON1) CONSTANTS MUST be registered as SYMBOLS. Ⓟ
* (RWR2) The lhs and rhs expressions of a REWRITE-RULE MUST be valid expressions in the notation of the algebra in which they are defined. Ⓗ
* (RWR3) REWRITE-RULE expressions MUST use only SYMBOLS or CONSTANTS within the same algebra. Ⓟ
* (FLU3) A newly constructed SYMBOL MUST have its string literal, and a name. Ⓟ
* (FLU4) The Fluent Builder pattern for SYMBOLS MUST support the following methods: `bp(n:int)`, `left()`, `right()`, `noassoc()`, `infix()`, `prefix()`, `postfix()`, `matchfix(close: token)`, `nofix()`, `constant()`, `commutative()`, `associative()`, `idempotent()`, `involutive()`, `shortCircuit()`, `identity(e: token)`, `annihilator(z: token)` Ⓟ
* (FLU5) A newly constructed REWRITE-RULE MUST have a name, a lhs expression, and a rhs expression. Ⓟ
* (FLU6) A newly constructed ALGEBRA-BLOCK MUST have a name. Ⓟ
* (FLU7) The Fluent Builder pattern for ALGEBRA-BLOCKS SHOULD support the following methods: `add()`, and `lookup()` Ⓟ
* (FLU8) The `add()` method of ALGEBRA-BLOCKS SHOULD support adding SYMBOLs and REWRITE-RULEs Ⓟ
* (FLU9) All SYMBOLS MUST be added to the ALGEBRA-BLOCK before REWRITE-RULEs within the Fluent Builder chain. Ⓗ
* (FLU10) All Classes in the fluent builder pattern SHOULD be frozen and immutable in a monadic style, so a single class can serve as both builder and product.

### Explicitly Prohibited Elements

* (P02) Mutable global state MUST NOT be introduced by an algebra block code. Ⓟ

### Example and Reference Binding Power Ranges

* (R01) Structural (`;` `,`): 0–9 Ⓝ
* (R02) Binders (`∀` `∃` `λ`): 10–19 Ⓝ
* (R03) Assignment and definitions (`≔` `:`): 20–29 Ⓝ
* (R04) Relations (`→` `↦` `⇒` `⟺`): 30–39 Ⓝ
* (R05) Comparisons and tests (`=` `<` `∈` `⊆`): 40–49 Ⓝ
* (R06) Coproducts (`∨` `∪` `⊕` `+`): 50–59 Ⓝ
* (R07) Products (`∧` `∩` `⊗` `*`): 60–69 Ⓝ
* (R08) Power operators (`^` `↑`): 70–79 Ⓝ
* (R09) Unary complement (`¬` `-` `∁`): 80–89 Ⓝ
* (R10) Application (`f[]`): 90–99 Ⓝ

### Verification

TBD
