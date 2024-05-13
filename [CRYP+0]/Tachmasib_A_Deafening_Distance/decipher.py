from random import randint
from itertools import cycle

p = 102639592829741105772054196573991675900716567808038066803341933521790711307779
g = 881

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

def main():
	P_A = int(input())
	P_B = int(input())
	X_A_1 = int(input())
	X_B_1 = int(input())
	K_1 = int(input())
	X_A_2 = int(input())
	X_B_2 = int(input())

	gXAB_1 = pow(g, X_A_1 * X_B_1, p)
	PAB_1 = (pow(modinv(P_A, p), X_B_1, p) * pow(modinv(P_B, p), X_A_1, p)) % p

	frw = (K_1 * modinv(gXAB_1 * PAB_1, p)) % p

	gXAB_2 = pow(g, X_A_2 * X_B_2, p)
	PAB_2 = (pow(modinv(P_A, p), X_B_2, p) * pow(modinv(P_B, p), X_A_2, p)) % p

	K_2 = (gXAB_2 * PAB_2 * frw) % p
	cflag = ""

	with open("./cipher_flag.txt", "r") as file:
		cflag = file.read()

	flag = xor(cflag, str(K_2))
	print(flag)

if __name__ == '__main__':
	main()