import random
import string

x = ''.join(random.choice(string.ascii_letters) for x in range(6)).upper()
print(x)
