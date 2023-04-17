My name is Rohan Dvivedi.

This project is built as a final project for course CSE 539 Applied Cryptography by Professor Jed Crandall.

This project may be used only by the professor in any way he desires, with or without any credits to the author, Rohan Dvivedi.

To use this project install as dependencies :
* `pip3 install numpy`
* `pip3 install gmpy2`
* `pip3 install crypto`
* `pip3 install pycrypto`
* `pip3 install cryptodome`
* `pip3 install cryptodomex`

You can run this project as `python3 secret_sharing.py`.
This project takes advantage of python's bignum implementation which is available in python 2.5+ and hence you must use python3 with this project.

Please refer to [Adi Shamir's How to share a secret? paper](https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf) for more information.

tasks
 * modify everything to use mod prime - sharing and reconstructing the secret must use mod p