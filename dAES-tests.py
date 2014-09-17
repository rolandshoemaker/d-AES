#!/usr/bin/env python
from __future__ import division

import dAES
import uuid, random, copy, timeit, sys

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def mean(stuff):
        return sum(stuff)/len(stuff)

def doubler(start, num):
	listy = []
	listy.append(start)
	for i in range(num-1):
		listy.append(listy[i]*2)
	return listy


def sboxDiff(SboxIn, SboxOut):
	diffBytes = 0
	for b, byte in enumerate(SboxIn):
		if not SboxOut[b] == byte:
			diffBytes += 1
	return diffBytes/len(SboxIn)

def bitFlip(key):
	flippedKeys = []
	for i in range(0, len(key), 2):
		bits = bin(int(key[i:i+2], base=16))
		for j, b in enumerate(bits[2:len(bits)]):
			flip = list(copy.deepcopy(bits[2:len(bits)]))
			flip[j] = (1)^int(b)
			bitStr = ""
			for f in flip:
				bitStr += str(f)
			flippedKey = copy.deepcopy(key)
			if not flippedKey[0:i-2]+hex(int(bitStr, base=2))[2:4] in flippedKeys and not flippedKey[0:i-2]+hex(int(bitStr, base=2))[2:4]+flippedKey[i:len(flippedKey)] in flippedKeys:
				if len(flippedKey[0:i-2]+hex(int(bitStr, base=2))[2:4]) == len(key):
					flippedKeys.append(flippedKey[0:i-2]+hex(int(bitStr, base=2))[2:4])#+flippedKey[i+2:len(flippedKey)])
				elif len(flippedKey[0:i-2]+hex(int(bitStr, base=2))[2:4]+flippedKey[i:len(flippedKey)]) == len(key) :
					flippedKeys.append(flippedKey[0:i-2]+hex(int(bitStr, base=2))[2:4]+flippedKey[i:len(flippedKey)])
	return flippedKeys

# Basic encryption tests
def basic_tests():
	print(colors.HEADER+"[Basic encryption tests]"+colors.ENDC)

	test_key = uuid.uuid4().hex+uuid.uuid4().hex # 256-bit (64 character) hex key
	print(colors.OKBLUE+"Generated 256-bit AES key: "+colors.WARNING+test_key+colors.ENDC)

	print(colors.OKBLUE+"Checking that two S-Boxes generated from the same key are equal..."+colors.ENDC)
	sbox_one = dAES.generateDynamicSbox(dAES.sboxOrig, dAES.hexToKey(test_key))
	sbox_two = dAES.generateDynamicSbox(dAES.sboxOrig, dAES.hexToKey(test_key))
	if not sbox_one==sbox_two:
		print(colors.OKBLUE+"\tS-Boxes aren't the same! "+colors.FAIL+"[FAILED]"+colors.ENDC)
		exit(1)
	print(colors.OKBLUE+"\tS-Boxes are the same "+colors.OKGREEN+"[PASSED]"+colors.ENDC)

	int_test_key = dAES.hexToKey(test_key)
	plain = uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex[0:random.randrange(0,32)]
	plaintwo = uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex[0:random.randrange(0,32)]
	print(colors.OKBLUE+"Generating "+str(len(plain))+" bytes of plaintext..."+colors.ENDC)
	print(colors.OKBLUE+"Encrypting plaintext..."+colors.ENDC)
	hard = dAES.encrypt(plain, int_test_key)
	hardtwo = dAES.encrypt(plain, int_test_key)
	if plain!=hard:
		print(colors.OKBLUE+"\tEncrypted ciphertext isn't the same as plaintext! "+colors.OKGREEN+"[PASSED]"+colors.ENDC)
	else:
		print(colors.OKBLUE+"\tEncrypted ciphertext is the same as plaintext! "+colors.FAIL+"[FAILED]"+colors.ENDC)
		exit(1)
	print(colors.OKBLUE+"Decrypting ciphertext..."+colors.ENDC)
	decd = dAES.decrypt(hard, int_test_key)
	if plain==decd:
		print(colors.OKBLUE+"\tDecrypted plaintext is the same as original plaintext! "+colors.OKGREEN+"[PASSED]"+colors.ENDC)
	else:
		print(colors.OKBLUE+"\tDecrypted plaintext isn't the same as original plaintext! "+colors.FAIL+"[FAILED]"+colors.ENDC)
		exit(1)
	print(colors.HEADER+"## All basic tests passed ##"+colors.ENDC)

# testing speed of enc and dec functions
def speed_tests(size):
	eSpeeds = []
	dSpeeds = []
	test_key = uuid.uuid4().hex+uuid.uuid4().hex # 256-bit (64 character) hex key
	plain = uuid.uuid4().hex*(size//32)
	e = timeit.Timer("dAES.encrypt('"+plain+"', dAES.hexToKey(\""+test_key+"\"))", "import dAES")
	eSpeeds = e.repeat(100, 1)
	if hasattr(sys, "pypy_translation_info"):
		print(colors.OKBLUE+"\tMean "+colors.OKGREEN+"enc"+colors.OKBLUE+" speed for "+str(len(plain))+" character string: "+colors.HEADER+str(round(mean(eSpeeds), 6))+"s"+colors.ENDC)		
	else:
		print(colors.OKBLUE+"\tMean "+colors.OKGREEN+"enc"+colors.OKBLUE+" speed for "+str(sys.getsizeof(plain))+" byte string: "+colors.HEADER+str(round(mean(eSpeeds), 6))+"s"+colors.ENDC)
	d = timeit.Timer("dAES.decrypt(\""+plain+"\", dAES.hexToKey(\""+test_key+"\"))", "import dAES")
	dSpeeds = e.repeat(100, 1)
	if hasattr(sys, "pypy_translation_info"):
		print(colors.OKBLUE+"\tMean "+colors.FAIL+"dec"+colors.OKBLUE+" speed for "+str(len(plain))+" character string: "+colors.HEADER+str(round(mean(dSpeeds), 6))+"s"+colors.ENDC)
	else:
		print(colors.OKBLUE+"\tMean "+colors.FAIL+"dec"+colors.OKBLUE+" speed for "+str(sys.getsizeof(plain))+" byte string: "+colors.HEADER+str(round(mean(dSpeeds), 6))+"s"+colors.ENDC)
	return [eSpeeds, dSpeeds]

# testing how different s-boxes actually are...
def sbox_tests(iters):
	# sbox tests
	print(colors.HEADER+"\n[Dynamic S-Box tests]"+colors.ENDC)
	test_key = uuid.uuid4().hex+uuid.uuid4().hex

	sbox_sim = []
	for i in range(iters):
		sbox_key = uuid.uuid4().hex+uuid.uuid4().hex
		sbox_keys = bitFlip(sbox_key)
		sbox_clean = dAES.generateDynamicSbox(dAES.sboxOrig, dAES.hexToKey(sbox_key))
		while len(sbox_keys) > 0:
			k = random.choice(sbox_keys)
			
			sbox_test = dAES.generateDynamicSbox(dAES.sboxOrig, dAES.hexToKey(k))

			diff = sboxDiff(sbox_clean, sbox_test)
			sbox_sim.append(diff)
			sbox_keys.pop(sbox_keys.index(k))
	print(colors.OKBLUE+"Tested "+str(len(sbox_sim))+" S-Boxes"+colors.ENDC)
	print(colors.OKBLUE+"\tMean difference: "+colors.OKGREEN+str(round(mean(sbox_sim)*100, 2))+"%"+colors.ENDC)
	print(colors.OKBLUE+"\tPercentage with no difference: "+colors.OKGREEN+str(round((sbox_sim.count(0)/len(sbox_sim))*100, 2))+"%"+colors.ENDC)
	return sbox_sim

if hasattr(sys, "pypy_translation_info"):
	print(colors.HEADER+"\t\t\t[pypy tests]"+colors.ENDC)
else:
	print(colors.HEADER+"\t\t\t[python tests]"+colors.ENDC)

basic_tests()

sbox_tests(100)

doubles = doubler(32, 15)

print(colors.HEADER+"\n[Speed tests]"+colors.ENDC)
print(colors.OKBLUE+"Testing encryption and decryption speeds for strings of length ["+colors.OKGREEN+", ".join(map(str, doubles))+colors.OKBLUE+"]"+colors.ENDC)
for i in doubles:
	speed_tests(i)
