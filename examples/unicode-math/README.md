# Mathematical Operator DSL — Pratt Parser Example

This example implements a small but complete mathematical DSL using a Pratt parser. The original DSL was designed to express **constraint specifications over measurement spaces** — requirements of the form "this measurement must fall within this admissible region" — but the parser and symbol table design is general enough to serve as a foundation for any symbolic mathematical language.

The key design goals are:

- Unicode symbols throughout, avoiding keyword collision with natural language
- A clean separation between parsing (CST production), rewriting (algebraic normalisation), and verification (SMT or other backends)
- An extensible symbol table organized into **algebra blocks**, each representing a coherent notational system
- A fluent builder API for symbol and rule registration that ports directly to OCaml, Python, Rust, or JavaScript

This is part of a larger project developing specification coding tools. This directory contains the specifications for the operator symbol table and some algebras.

---

## Parser

The parser is assumed to be a Pratt parser (top-down operator precedence parser). All operator behavior is encoded in the symbol table, not the parser logic.

Each token is either:

- an **atom** — an identifier, number, or constant
- an **operator** — with known fixity, binding power, and associativity

Adding a new operator means registering it in the symbol table. The parser loop never changes and is not disturbed by new operators.

### Fixity

Every operator has a **fixity** describing its syntactic position:

| fixity | description | example |
|---|---|---|
| `infix` | between two expressions | `a ∧ b` |
| `prefix` | before one expression | `¬ a` |
| `postfix` | after one expression | `n !` |
| `matchfix` | wraps one expression with an open and close token | `( a )`, `{ a }`, `[ a ]` |

### Binding Power and Associativity

Every operator can have a **binding power** given as a positive integer. Higher binding power means tighter binding. The binding power numbers follow a range convention so that operator classes can be identified by range:

| range | class | examples |
|---|---|---|
| 0-9 | structural sequencing | `;` `,` |
| 10-19 | binders | `∀` `∃` `λ` |
| 20-29 | assignment and relations | `≔` `:` |
| 30-39 | relations (arrows) | `→` `↦` `⇒` `⟺`|
| 40-49 | comparisons and tests | `=` `<` `∈` `⊆` |
| 50-59 | coproducts | `∨` `∪` `⊕` `+` |
| 60-69 | products | `∧` `∩` `⊗` `*` |
| 70-79 | power operators | `^` `↑` |
| 80-89 | unary complement | `¬` `-` `∁` |
| 90-99 | application | `f[]` |

Associativity is one of:

| associativity | meaning |
|---|---|
| `left` | `a op b op c` → `(a op b) op c` |
| `right` | `a op b op c` → `a op (b op c)` |
| `none` | `a op b op c` is a parse error (no chaining) |

### Chained Associativity

For comparison and relation operators, sequences like `a < b < c` or `A ⊆ B ⊆ C` are mathematically natural and mean something specific: each consecutive pair satisfies the relation, and the middle term is shared in a **chain**.

Chaining is not standard left or right associativity and should be handled as a separate **rewrite rule** applied to the concrete syntax tree after parsing. For example the parser produces a raw right-associated tree and a subsequent rewrite pass expands `a op1 b op2 c` into `(a op1 b) ∧ (b op2 c)`, sharing the middle term `b`. Note, the combining operator (here `∧`) is a property of the algebra block, not of the individual symbol.

### Matchfix Operators

Matchfix operators  like `()` or `{}` use the opening token as an operator symbol and specify the closing token as an attribute. They are handled by the parser as a special case of prefix: consume the opening token, parse an inner expression at minimum binding power, then expect the closing token.

If the operator is also given a binding power then it will also be parsed as a binary operator with the inner expression as the right argument. For example `f[x, y]` will be parsed as something like `binary(f, list(x, list(y, nil)))`.

---

## Symbol Table

Each symbol is registered with its full set of attributes. The format uses a fluent builder chain for portability.

### Symbol Attributes

| attribute | meaning |
|---|---|
| `bp(n:int)` | binding power |
| `left()` / `right()` / `none()` | associativity |
| `infix()` / `prefix()` / `postfix()` / `matchfix(close: token)` | fixity |
| `constant()` | nullary atom |
| `commutative()` | `a op b = b op a` |
| `associative()` | `(a op b) op c = a op (b op c)` |
| `idempotent()` | `a op a = a` |
| `involutive()` | applying twice is identity (`¬¬a = a`) |
| `shortCircuit()` | evaluation can stop early (useful to evaluator) |
| `identity(e: token)` | `a op e = a` |
| `annihilator(z: token)` | `a op z = z` |

Distributivity, De Morgan laws, absorption, and chaining could have been attributes here but as they are properties of an algebra as a whole they are better implemented as rewrite rules registered on the algebra block.

---

## Algebra Blocks

Symbols are not registered in a flat global table. They are grouped into **algebra blocks**. This reflects the mathematical reality that symbols have meaning only within a notational system, and that algebraic laws (distributivity, De Morgan, chaining) are properties of the system, not of individual symbols.

Each algebra block contains:

- **symbols** — registered with their attributes
- **constants** — nullary atoms belonging to the algebra that should be tagged early
- **rewrite rules** — algebraic identities expressed as expressions in the algebra's own language

The intent for rewrite rules is that they are parsed by the same parser being bootstrapped. If the parser cannot parse its own rule patterns, something is fundamentally broken, while rules that require direct AST construction are tree optimisations, not rewrite rules.

###  Example Blocks

#### Structural

| sym | name | bp | assoc | fixity | attributes |
|---|---|---|---|---|---|
| `,` | list | 15 | right | infix | |
| `;` | sequence | 10 | right | infix | |
| `≔` | define | 20 | right | infix | |
| `:` | type | 20 | right | infix | |
| `∀` | forall | 5 | right | prefix binder | |
| `∃` | exists | 5 | right | prefix binder | |
| `(` | parentheses | — | — | matchfix `)` | |
| `{` | set-literal | — | — | matchfix `}` | |
| `[` | apply | 95 | — | matchfix `]` | |

#### Logic

| sym | name | bp | assoc | fixity | attributes |
|---|---|---|---|---|---|
| `∧` | and | 45 | left | infix | commutative, associative, idempotent, shortCircuit |
| `∨` | or | 35 | left | infix | commutative, associative, idempotent, shortCircuit |
| `¬` | not | 90 | — | prefix | involutive |
| `⇒` | implies | 25 | right | infix | |
| `⟺` | iff | 25 | none | infix | commutative |
| `⊤` | true | — | — | constant | |
| `⊥` | false | — | — | constant | |

| rule | lhs | rhs |
|---|---|---|
| distributivity-and | `a∧(b∨c)` | `(a∧b)∨(a∧c)` |
| distributivity-or | `a∨(b∧c)` | `(a∨b)∧(a∨c)` |
| de-morgan-and | `¬(a∧b)` | `¬a∨¬b` |
| de-morgan-or | `¬(a∨b)` | `¬a∧¬b` |
| absorption-and | `a∧(a∨b)` | `a` |
| absorption-or | `a∨(a∧b)` | `a` |
| chain-implies | `a⇒b⇒c` | `(a⇒b)∧(b⇒c)` |

---

## Example Specification

This was originally designed as part of a larger specification language. For example:

```text
Battery ∈ 𝒮

runtime : Battery → ℝ[hr]

Runtime_OK ≔ { t ∈ ℝ[hr] | t ≥ 1 hr }

∀ b ∈ Battery ; runtime(b) ∈ Runtime_OK
```
