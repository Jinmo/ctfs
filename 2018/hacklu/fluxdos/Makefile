# TOP LEVEL COMMANDS

all: target/binary.rom

clean:
	rm target/binary.rom

# test locally
test: all
	echo flag{guru_meditation_flag_found} > flag.txt
	bin/fluxdos target/binary.rom > output.txt
	python src/parse.py output.txt

target/binary.rom: src/string.bst src/main.bst
	bin/beast build

src/string.bst: src/gen_string_bst.py
	python src/gen_string_bst.py src/string.bst 'flag.txt'