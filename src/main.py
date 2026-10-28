import tokenizer

example = """
read> a;
read> b;
read> c;
d=c*a;
if [d*2-3.5] {
    while [b-5] {
        a = a + 2 * c
        b = b - 1
    }
}
"""
tokenzr = tokenizer.Tokenizer()
print(*tokenzr.tokenize(example), sep='\n')