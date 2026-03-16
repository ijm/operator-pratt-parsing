<!-- markdownlint-disable MD041 -->
## operator pratt parsing

Generic functional Pratt parsing operator expressions.

This repo in in the process of being populated from a private repo as I clean up and verify things.

This is part of a larger Spec Coding project (link-to-come). The source files in this repo are files like .spec and .prompt and NOT code source files. Unless specifiacly highlighted all source files are LLM generated from their respective .fullprompt files.

Much is still done by hand, so for example the generated files are not hash-chained to their prompts.

## operator-pratt-parsing

A pure, functional, non-recursive Pratt parser. Implemented in OCaml and Python.

## What this is

A Pratt parser (top-down operator precedence parsing, Vaughan Pratt 1973) turns a flat sequence of tokens into an expression tree, respecting operator precedence, associativity, and grouping. The classic formulation is recursive. This implementation is zipper-like and not recursive.

The core of the parser is a single fold over the token list:

```ocaml
let parse toks =
  finish (List.fold_left step { focus = Hole; stack = []; min_bp = 0 } toks)
```

`step` is a pure function from `zipper * token` to `zipper`. There is no mutable state, no parser monad, no lookahead, no backtracking. Each token is consumed exactly once, in order, and immediately discharged.

## Design philosophy

**Pure and functional.** `step` and `reduce` are total functions over algebraic types. No references, no mutable state, no side effects. The parse state is a plain value you can inspect, copy, serialize, or diff at any point.

**No lookahead.** Each call to `step` sees exactly one token: the head of the remaining list. No peeking or lookahead is required. The zipper-like accumulator carries everything needed to make the right decision.

**No recursion.** The classic Pratt formulation recurses into subexpressions to handle precedence. Here that recursion is made explicit: the call stack is replaced by a zipper-like accumulator that represents the parse-in-progress as a first-class value. `reduce` is tail-recursive. `step` does not recurse at all.

**Errors are values.** Parse errors are represented as `Error` nodes in the expression type, not exceptions. The error carries the full zipper state at the point of failure, making post-mortem diagnosis straightforward. The parser never throws; it always returns a tree.

**Separation of concerns.** This module knows nothing about your language. Tokens are classified into their syntactic roles (`Literal`, `Prefix`, `Infix`, `Open`, `Close`, `Postfix`) before being handed to the parser. The `lookup` function that does that classification lives entirely outside this module. The parser only manipulates structure.

**Language-independent design.** The implementation is deliberately algebraic.
The Python port mirrors the OCaml structure closely.

## The accumulator

The fold accumulator is a `zipper`:

```ocaml
type 'tok zipper = {
  focus  : 'tok expr;        (* the subtree currently under construction *)
  stack  : 'tok frame list;  (* suspended contexts above the focus *)
  min_bp : int;              (* binding power threshold for the current scope *)
}
```

The `stack` is a list of suspended frames, each representing a node whose children are not yet complete:

```ocaml
type 'tok frame =
  | FUnary  of 'tok * int               (* op, saved min_bp *)
  | FBinary of 'tok * 'tok expr * int   (* op, left child, saved min_bp *)
  | FGroup  of 'tok * 'tok * int        (* open token, expected close, saved min_bp *)
```

This is zipper-like in the sense that the stack is the path back to the root of the tree-under-construction, and `focus` is the currently active subtree. It is not a true zipper until `finish` is called and the complete tree exists; during the fold it is better understood as a sub-parse continuation.

`Hole` in the expression type marks positions that have been allocated but not yet filled.  This makes the "waiting for an operand" state explicit in the type rather than implicit in control flow and recursion.

## Token classification

Tokens are classified before parsing:

```ocaml
type 'tok token_t =
  | Literal  of 'tok
  | Prefix   of 'tok * int                      (* op, binding power *)
  | Postfix  of 'tok * int                      (* op, binding power *)
  | Infix    of 'tok * int * associativity      (* op, bp, assoc *)
  | Open     of 'tok * 'tok * int option        (* open tok, close tok, infix_bp *)
  | Close    of 'tok
```

`Open` carries its matching close token, enabling proper bracket verification at parse time. The optional `infix_bp` on `Open` handles juxtaposition operators like function application: `f(x)` where `(` appears with something to its left and should behave as a binary operator binding `f` to its argument group.

Associativity is `Left | Right | Noassoc`. Non-associative operators produce an error if chained without explicit grouping.

## What the parser handles

- Literal values
- Prefix (unary) operators: `-x`, `not p`, `~bits`
- Postfix (unary) operators: `x!`, `p?`
- Binary infix operators with arbitrary precedence and associativity
- Matchfix grouping operators: `(...)`, `[...]`, `{...}` or any matched pair
- Juxtaposition / function application: `f(args)`, `a[i]` where the open bracket acts as an infix operator binding the left-hand expression into the group

## What it does not handle

- Mixfix operators beyond matchfix (e.g. `if _ then _ else _`) : better handled in a subsequent pass over the tree
- Operator chaining (`1 < 2 < 3` → `Chain`) : left to a post-parse tree pass, where it can be handled with full type and context information
- Token stream construction : bring your own tokenizer and `lookup` function

## Worked example

Given a `lookup` table where `+` is left-associative at bp 10, `*` at bp 20, `^` is right-associative at bp 30, and `-` is prefix at bp 100:

```text
tokens:  - 2 ^ 3 * 4 + 5
result:  Binary(+, Binary(*, Unary(-, Binary(^, Lit 2, Lit 3)), Lit 4), Lit 5)
```

i.e. `(((-2)^3) * 4) + 5` with precedence and associativity resolved correctly, with no recursion and no lookahead.

## Interface

The public interface is a single function:

```ocaml
(* OCaml *)
val parse : 'tok token_t list -> 'tok expr
```

```python
# Python
def parse(toks: list[TokenT]) -> Expr:
```

Feed it a classified token list, receive an expression tree. Errors are `Error` nodes within the tree; a well-formed input produces a tree containing no `Error` or `Hole` nodes.

## Relationship to the classic formulation

The classic Pratt loop:

```text
parse_expr(min_bp):
  left = nud(next())
  while peek().bp > min_bp:
    left = led(next(), left)
  return left
```

recurses into `nud` and `led` to handle subexpressions, using the call stack as an implicit list of suspended contexts. This implementation makes that list explicit as the zipper's `stack` field, turns the recursion into a fold, and makes the intermediate parse state a first-class value. The correspondence is direct: pushing an `FBinary` frame is entering a `led` call; `reduce` firing is returning from one.
