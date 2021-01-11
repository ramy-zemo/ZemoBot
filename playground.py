def effify(non_f_str: str):
    return eval(f'f"""{non_f_str}"""')

y = " Ich komm einfach mit."
x = "Test {y}"

print(x)

print(effify(x))
