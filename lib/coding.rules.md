<!-- markdownlint-disable MD041 -->
## Coding Rules <!-- that haven't made it into the spec yet -->

* If you make any non-trivial design decisions output them separately as a well formed JSON array.
* Prefer the simplest standard library tool that satisfies the requirement.
* Do not introduce abstractions not implied by the spec.
* Do not choose more elaborate option just because it looks more considered - elegance and simplicity are much more valuable than superficial appearances.
* Write the minimum code that correctly expresses the specification. Do not introduce intermediate variables, lists, or loops where an API or existing methods already provides a way to express the same thing directly.
* Ignore circle-letter verification markers, they are for post-generation validation only.
