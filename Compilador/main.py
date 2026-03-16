from AnalizadorLexico import Lexer
import sys
from copy import copy
import os.path


print("\t\t\t\t*  Compiler for the language Juan Pato v0.1   *")
print("\t\t\t\t------------------------------------------------------\n")

print("\nInput the name of the source program (default: holamundo.jp) or 'exit' to exit:\n")

base_dir = os.path.dirname(os.path.abspath(__file__))
src_file = sys.stdin.readline().rstrip()

if src_file == "":
    src_file = "holamundo.jp"
elif src_file == "exit":
    print("\nCompiler terminated.\n")
    exit()

target_path = os.path.join(base_dir, "programas", src_file)

if not os.path.isfile(target_path):
    print(f'\nThe program "{src_file}" does not exist.\nCompiler terminated.\n')
    exit()

programa_fuente = open(target_path, 'r', encoding='utf-8').read()

etapa = 6
while etapa < 1 or etapa > 5:
    print("\nSelect compilation stage:\n")
    print("(1) Lexical analysis\n")

    try:
        etapa = int(sys.stdin.readline().rstrip())
    except:
        etapa = 6

    if etapa == "":
        etapa = 1


if etapa >= 1:

    lexer = Lexer().get_lexer()

    print("\n====================================================")
    print("               LEXICAL ANALYSIS STARTED             ")
    print("====================================================\n")

    print("Source Program:\n")
    print("------------------------------------------")
    print(programa_fuente)
    print("------------------------------------------\n")

    tokens = list(lexer.lex(programa_fuente))

    print("Tokens Identified:\n")

    print("{:<20} {:<20}".format("TOKEN TYPE", "VALUE"))
    print("-" * 40)

    contador = 0

    for token in tokens:
        print("{:<20} {:<20}".format(token.name, token.value))
        contador += 1

    print("-" * 40)
    print(f"Total tokens identified: {contador}\n")

    print("Lexical analysis completed.\n")
