from random import randint
from itertools import cycle

p = 102639592829741105772054196573991675900716567808038066803341933521790711307779
g = 881

text = "QWERTYUIOPASDFGHJKLZXCVBNM"
flag = "flag{test_flag_jeopardy_0}"

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def xor(message, key):
	return ''.join(chr(ord(c)^ord(k)) for c,k in zip(message, cycle(key)))

def genSessionKey(a_A, a_B, P_A, P_B):
	R_A = randint(1, p - 1)
	R_B = randint(1, p - 1)
	X_A = (a_A + R_A) % (p - 1)
	X_B = (a_B + R_B) % (p - 1)

	print(f"X_1: {X_A}\nX_2: {X_B}\n")

	K = pow((pow(g, X_B, p) * modinv(P_B, p)), R_A, p)

	return K


def main():
	a_A = randint(1, p - 1)
	a_B = randint(1, p - 1)

	P_A = pow(g, a_A, p)
	P_B = pow(g, a_B, p)

	print(f"P_1: {P_A}\nP_2: {P_B}\n")

	K_1 = genSessionKey(a_A, a_B, P_A, P_B)
	K_1 = str(K_1)
	print(f"K_1: {K_1}\n")
	ctext = xor(text, K_1)
	newtext = ""

	with open("./test_cipher_text.txt", "w") as file:
		file.write(ctext)

	with open("./test_cipher_text.txt", "r") as file:
		newtext = file.read()

	ptext = xor(newtext, K_1)

	print(f"ctext: {ctext}\nptext: {ptext}\n")

	K_2 = genSessionKey(a_A, a_B, P_A, P_B)
	K_2 = str(K_2)
	ctext = xor(flag, K_2)
	newtext = ""

	with open("./new_trajectory.txt", "w") as file:
		file.write(ctext)

	with open("./new_trajectory.txt", "r") as file:
		newtext = file.read()

	ptext = xor(newtext, K_2)

	print(f"ctext: {ctext}")

if __name__ == '__main__':
	main()