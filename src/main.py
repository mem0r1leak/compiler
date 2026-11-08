import tokenizer
import codegen

example = """
read> a;
read> b;
read> c;
d=c*a;
if [d*2-3.5] {
    while [b-5] {
        a = a + 2 * c;
        b = b - 1;
    }
}
write> a;
"""

code = """
read> a;
read> b;
read> c;
"""

tokenizer = tokenizer.Tokenizer()
tokens = tokenizer.tokenize(example)
codegen = codegen.Codegen(tokens, example)
codegen.translate()
print(*codegen.get_instructions(), sep='\n')
