L=../../../lib

PYCODESPEC=$L/coding-python-spec.md
PYCODEEXTRA=$L/coding.rules.md

all: algebra_block.fullprompt structural.alg.fullprompt set-theory.alg.fullprompt

algebra_block.fullprompt: algebra_block.prompt ../algebra-blocks.spec.md \
                          $(PYCODEEXTRA) $(PYCODESPEC)
	$L/catwrap.py \
		-o $@ \
		-p algebra_block.prompt \
		$(PYCODEEXTRA) ../algebra-blocks.spec.md $(PYCODESPEC)

%.pyi: %.py
	stubgen --include-docstrings --output . $<

%.alg.fullprompt: ../%.alg.md mkpyblock.prompt algebra_block.pyi \
                  $(PYCODEEXTRA) $(PYCODESPEC)
	$L/catwrap.py \
		-o $@ \
		-p mkpyblock.prompt \
		$(PYCODEEXTRA) $< algebra_block.pyi $(PYCODESPEC)