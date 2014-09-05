#!/usr/bin/python3

import dAES
import uuid

test_key = uuid.uuid4().hex+uuid.uuid4().hex # 256-bit (64 character) hex key
int_test_key = dAES.hexToKey(test_key)
print("test key: "+test_key)
plain = uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex+uuid.uuid4().hex
print("input data: "+plain)
hard = dAES.encrypt(plain, int_test_key)
print("plaintext != ciphertext? "+str(plain!=hard))
decd = dAES.decrypt(hard, int_test_key)
print("input plaintext == output plaintext? "+str(plain==decd))
print("output data: "+decd)

