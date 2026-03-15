# ALGEBRA-BLOCK: `set-theory`

Unicode set-theoretic operators, relations, and constants.

## Symbols

| Glyph | Name       | Fixity  | BP | Associativity | Flags                               | Identity | Annihilator |
|-------|------------|---------|----|---------------|-------------------------------------|----------|-------------|
| `∪`   | union      | infix   | 52 | left          | commutative, associative, idempotent | `∅`     | `𝒰`        |
| `∩`   | inter      | infix   | 62 | left          | commutative, associative, idempotent | `𝒰`     | `∅`        |
| `∖`   | setminus   | infix   | 61 | left          |                                     |          |             |
| `∁`   | complement | prefix  | 82 |               | involutive                          |          |             |
| `𝒫`   | powerset   | prefix  | 72 |               |                                     |          |             |
| `∈`   | elem       | infix   | 45 | left          |                                     |          |             |
| `∉`   | notelem    | infix   | 45 | left          |                                     |          |             |
| `⊆`   | subseteq   | infix   | 44 | left          |                                     |          |             |
| `⊂`   | subset     | infix   | 43 | left          |                                     |          |             |
| `⊇`   | supseteq   | infix   | 44 | left          |                                     |          |             |
| `⊃`   | supset     | infix   | 43 | left          |                                     |          |             |
| `∅`   | emptyset   |         |    |               | constant                            |          |             |
| `𝒰`   | universe   |         |    |               | constant                            |          |             |

## Rewrite Rules

| Name                  | LHS              | RHS              |
|-----------------------|------------------|------------------|
| demorgan-union        | `∁(A ∪ B)`       | `∁A ∩ ∁B`       |
| demorgan-inter        | `∁(A ∩ B)`       | `∁A ∪ ∁B`       |
| double-complement     | `∁(∁A)`          | `A`              |
| complement-union      | `A ∪ ∁A`         | `𝒰`             |
| complement-inter      | `A ∩ ∁A`         | `∅`             |
| complement-universe   | `∁𝒰`            | `∅`             |
| complement-empty      | `∁∅`             | `𝒰`             |
| absorption-union      | `A ∪ (A ∩ B)`    | `A`              |
| absorption-inter      | `A ∩ (A ∪ B)`    | `A`              |
| identity-union        | `A ∪ ∅`          | `A`              |
| identity-inter        | `A ∩ 𝒰`          | `A`              |
| annihilator-union     | `A ∪ 𝒰`          | `𝒰`             |
| annihilator-inter     | `A ∩ ∅`          | `∅`             |
| idempotent-union      | `A ∪ A`          | `A`              |
| idempotent-inter      | `A ∩ A`          | `A`              |
| setminus-def          | `A ∖ B`          | `A ∩ ∁B`        |

