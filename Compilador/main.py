from AnalizadorLexico import Lexer
import sys
from copy import copy, deepcopy
import os.path


print("\t\t\t\t*  Compiler for the language Juan Pato v0.1   *")
print("\t\t\t\t------------------------------------------------------\n\n")
print("\033[0m")

print("\ninput the name of the source program (default: holamundo.jp) or 'exit' to exit:\n")
base_dir = os.path.dirname(os.path.abspath(__file__))
src_file = sys.stdin.readline()
src_file = src_file.rstrip()
if src_file == "":
    src_file = "holamundo.jp"
elif  src_file == "exit":
    print("\033[92m\nCompiler terminated.\n")
    exit()

target_path = os.path.join(base_dir, "programas", src_file)
print (target_path)
if not os.path.isfile(target_path):
  print("\nthe program \""+src_file+"\" does not exist.\033[92m\n\nCompiler terminated.\n")
  exit()
programa_fuente = open(target_path, 'r', encoding='utf-8').read()
etapa = 6
while etapa < 1 or etapa > 5:
    print("\n* Input the number of the stage up to which you would like to execute the compilation proccess:\n")
    print("(1) Lexical analysis\n")
    try:
        etapa = sys.stdin.readline()
        etapa = int(etapa.rstrip())
    except:
        etapa = 6
    if etapa == "":
        etapa = 1
if etapa >= 1:

    lexer = Lexer().get_lexer()
    print("\033[92m\n----------------------------------------------------")
    print("Starting lexical analysis")
    print("----------------------------------------------------\n\033[0m")
    print("\nSource program:\n\033[96m")
    print(programa_fuente)
    print('\033[0m')
    tokens = lexer.lex(programa_fuente)
    print("\nIdentified tokens:\n\033[93m")

    for token in copy(tokens):
        print(token)
