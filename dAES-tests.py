#!/usr/bin/python3

import dAES
import uuid, random, copy

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def mean(stuff):
        return sum(stuff)/len(stuff)

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
			#if j < len(flip)-1:
			#	flip[j+1] = (1)^int(b)
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
	int_test_key = dAES.hexToKey(test_key)
	print(colors.OKBLUE+"Generating 512 bits of plaintext..."+colors.ENDC)
	plain = uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex
	print(colors.OKBLUE+"Encrypting plaintext..."+colors.ENDC)
	hard = dAES.encrypt(plain, int_test_key)
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

def sbox_tests():
	# sbox tests
	iters = 100
	sbox_sim = []
	for i in range(iters):
		sbox_key = uuid.uuid4().hex+uuid.uuid4().hex
		#print(str(len(sbox_key)))
		#print("a: "+str(len(sbox_key)))
		sbox_keys = bitFlip(sbox_key)
		#print(sbox_keys)
		#print("b: "+str(len(sbox_keys[random.randrange(len(sbox_keys))])))
		while len(sbox_keys) > 0:
			k = random.choice(sbox_keys)
			#print(dAES.hexToKey(k))
			sbox_clean = dAES.generateDynamicSbox(dAES.sboxOrig, dAES.hexToKey(sbox_key))
			#print(dAES.hexToKey(sbox_key))
			sbox_test = dAES.generateDynamicSbox(dAES.sboxOrig, dAES.hexToKey(k))
			diff = sboxDiff(sbox_clean, sbox_test)
			#print(str(diff))
			sbox_sim.append(diff)
			sbox_keys.pop(sbox_keys.index(k))
	print("mean difference: "+str(round(mean(sbox_sim)*100, 2))+"%")
	print("percentage with no difference: "+str(round((sbox_sim.count(0)/len(sbox_sim))*100, 2))+"%")

basic_tests()