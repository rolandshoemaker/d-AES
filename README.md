d-AES
=====

**Note:** This is not mean't to be fast. As I work I'll try to optimize to the best of my ability but this is above all a **POC** implementation of dynamic S-Boxes! (It is **MUCH** faster under PyPy for larger plaintext sizes! and slightly slower for smaller ones... see the speed tests section)

A pure python3(/2.7) implementation of the Rijndael cipher (AES) based on Brandon Sterne's python2.5 [implementation](http://brandon.sternefamily.net/2007/06/aes-tutorial-python-implementation/) that additionally implements modifications to the AES Cipher suggested in various academic papers to dynamically generate S-Boxes from the cipher key instead of using the fixed Rijndael S-Box.

I am using the Hosseinkhani-Javadi method to generate the S-Box, although using all 256 bits of the key instead of just the first 128 to perform two rounds in a similar fashion to a block cipher.

One possible attack method would be to generate all possible S-Boxes from all possible 256 bit AES keys and apply them during the `subBytes` step as suggested by Hosseikhani and Javadi, but the number of possible S-Boxes is somewhere around 10 to the power of 38, factorial ((10^38)!) choices for 128-bits of key. By mixing a full 256 bit key with itself and using each 128 bit half of the key for two rounds of the `sboxRound` function we increase the number of possible S-Boxes to 2^256. 

Example
-------
	test_key = "f4eba54dab7b4cdcb34f13689beea128acdc8960c8ec4c929d0c9f85d2fa5c22" # 256-bit (64 character) hex key
	int_test_key = dAES.hexToKey(test_key)
	plain = "blahblahblahblah i like really weirdly secure AES techniques!"
	cipher = dAES.encrypt(plain, int_test_key)
	decryptedPlain = dAES.decrypt(cipher, int_test_key)

Visulization
------------
Over ~650,000 iterations
![Scatter plot of difference between sbox generated from key and sbox generated from same key with flipped bit](scatter-graph.png)
![Histogram of difference between sbox generated from key and sbox generated from same key with flipped bit](hist-graph.png)

Speed tests
-----------

These mean speeds are based on running the `speed_tests` function from `dAES-tests.py` on my random ol' server (so take them with a grain of salt...) Each time is a mean time over 100 iterations with each different plaintext size `[32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288]` (Also note that OFB encryption and decryption cannot be parallelized, so yeah.)

	rolands@kamaji:~/utils/dAES$ python dAES-tests.py
	mean encryption speed for 32 character string:		0.00114s
	mean decryption speed for 32 character string:		0.00112s
	mean encryption speed for 64 character string:		0.001855s
	mean decryption speed for 64 character string:		0.00185s
	mean encryption speed for 128 character string:		0.003317s
	mean decryption speed for 128 character string:		0.003313s
	mean encryption speed for 256 character string:		0.006288s
	mean decryption speed for 256 character string:		0.006584s
	mean encryption speed for 512 character string:		0.012169s
	mean decryption speed for 512 character string:		0.010772s
	mean encryption speed for 1024 character string:	0.020697s
	mean decryption speed for 1024 character string:	0.020661s
	mean encryption speed for 2048 character string:	0.040693s
	mean decryption speed for 2048 character string:	0.040577s
	mean encryption speed for 4096 character string:	0.085646s
	mean decryption speed for 4096 character string:	0.083073s
	mean encryption speed for 8192 character string:	0.164645s
	mean decryption speed for 8192 character string:	0.1622s
	mean encryption speed for 16384 character string:	0.324669s
	mean decryption speed for 16384 character string:	0.326186s
	mean encryption speed for 32768 character string:	0.649447s
	mean decryption speed for 32768 character string:	0.6676s
	mean encryption speed for 65536 character string:	1.331664s
	mean decryption speed for 65536 character string:	1.323691s
	mean encryption speed for 131072 character string:	2.65424s
	mean decryption speed for 131072 character string:	2.640893s
	mean encryption speed for 262144 character string:	5.243996s
	mean decryption speed for 262144 character string:	5.227484s
	mean encryption speed for 524288 character string:	10.681648s
	mean decryption speed for 524288 character string:	10.597086s

	rolands@kamaji:~/utils/dAES$ pypy dAES-tests.py
	mean encryption speed for 32 character string:		0.002973s
	mean decryption speed for 32 character string:		0.001345s
	mean encryption speed for 64 character string:		0.001117s
	mean decryption speed for 64 character string:		0.000838s
	mean encryption speed for 128 character string:		0.000915s
	mean decryption speed for 128 character string:		0.00093s
	mean encryption speed for 256 character string:		0.001026s
	mean decryption speed for 256 character string:		0.00089s
	mean encryption speed for 512 character string:		0.001667s
	mean decryption speed for 512 character string:		0.001631s
	mean encryption speed for 1024 character string:	0.003121s
	mean decryption speed for 1024 character string:	0.003104s
	mean encryption speed for 2048 character string:	0.005381s
	mean decryption speed for 2048 character string:	0.005349s
	mean encryption speed for 4096 character string:	0.010716s
	mean decryption speed for 4096 character string:	0.011091s
	mean encryption speed for 8192 character string:	0.021394s
	mean decryption speed for 8192 character string:	0.021311s
	mean encryption speed for 16384 character string:	0.042622s
	mean decryption speed for 16384 character string:	0.044081s
	mean encryption speed for 32768 character string:	0.085557s
	mean decryption speed for 32768 character string:	0.086141s
	mean encryption speed for 65536 character string:	0.177523s
	mean decryption speed for 65536 character string:	0.175356s
	mean encryption speed for 131072 character string:	0.338576s
	mean decryption speed for 131072 character string:	0.337783s
	mean encryption speed for 262144 character string:	0.693953s
	mean decryption speed for 262144 character string:	0.677284s
	mean encryption speed for 524288 character string:	1.354397s
	mean decryption speed for 524288 character string:	1.360687s

	rolands@kamaji:~/utils/dAES$ lscpu
	Architecture:          x86_64
	CPU op-mode(s):        32-bit, 64-bit
	Byte Order:            Little Endian
	CPU(s):                24
	On-line CPU(s) list:   0-23
	Thread(s) per core:    2
	Core(s) per socket:    6
	Socket(s):             2
	NUMA node(s):          2
	Vendor ID:             GenuineIntel
	CPU family:            6
	Model:                 44
	Stepping:              2
	CPU MHz:               1600.000
	BogoMIPS:              5331.76
	Virtualization:        VT-x
	L1d cache:             32K
	L1i cache:             32K
	L2 cache:              256K
	L3 cache:              12288K
	NUMA node0 CPU(s):     0,2,4,6,8,10,12,14,16,18,20,22
	NUMA node1 CPU(s):     1,3,5,7,9,11,13,15,17,19,21,23

Academic Papers
---------------

* [Using Cipher Key to Generate Dynamic S-Box in AES Cipher System](http://cscjournals.org/csc/manuscript/Journals/IJCSS/volume6/Issue1/IJCSS-630.pdf) by R. Hosseinkhani and H. Haj Seyyed Javadi
* [IMPLEMENTATION OF STRONGER AES BY USING DYNAMIC S-BOX DEPENDENT OF MASTER KEY](http://www.jatit.org/volumes/Vol53No2/6Vol53No2.pdf) by S. Arrag, A. Hamdoun, A, Tragha, and S. Eddine Khamlich
* [Generation of AES Key Dependent S-Boxes using RC4 Algorithm](http://www.mtc.edu.eg/asat13/pdf/ce24.pdf) by Abd-ElGhafar, A. Rohiem, A. Diaa, and F. Mohammed
* [Dynamic Substitution Box](http://shodhganga.inflibnet.ac.in/bitstream/10603/5051/12/12_chapter%203.pdf)
