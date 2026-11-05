#
# Copyright (c) 2014-2015 Sylvain Peyrefitte
#
# This file is part of rdpy.
#
# rdpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
Wrapper around RSA library
"""

import os
import rsa

def _bytes2int(b):
    if isinstance(b, str):
        b = b.encode("latin-1")
    return int.from_bytes(bytes(b), "big")

def _int2bytes(i, fill_size = None):
    size = max(1, (i.bit_length() + 7) // 8)
    if fill_size is not None:
        size = max(size, fill_size)
    return i.to_bytes(size, "big")

def newkeys(size):
    """
    @summary: wrapper around rsa.newkeys function
    @param size: {integer} size of key
    """
    return rsa.newkeys(size)

def PublicKey(e, n):
    """
    @param e: {long | str}public exponent
    @param n: {long | str}modulus
    """
    if isinstance(e, (str, bytes)):
        e = _bytes2int(e)
    if isinstance(n, (str, bytes)):
        n = _bytes2int(n)
    return { 'e' : e, 'n' : n }

def PrivateKey(d, n):
    """
    @param d: {long | str}private exponent
    @param n: {long | str}modulus
    """
    if isinstance(d, (str, bytes)):
        d = _bytes2int(d)
    if isinstance(n, (str, bytes)):
        n = _bytes2int(n)
    return { 'd' : d, 'n' : n }

def int2bytes(i, fill_size=None):
    """
    @summary: wrapper of rsa.transform.int2bytes
    """
    return _int2bytes(i, fill_size)

def random(size):
    """
    @summary: wrapper around rsa.randnum.read_random_bits function
    @param size: {integer] size in bits
    @return: {str} random bytes array
    """
    return os.urandom(size // 8)

def encrypt(message, publicKey):
    """
    @summary: wrapper around rsa.core.encrypt_int function
    @param message: {str} source message
    @param publicKey: {rsa.PublicKey}
    """
    return _int2bytes(pow(_bytes2int(message), publicKey['e'], publicKey['n']), (publicKey['n'].bit_length() + 7) // 8)

def decrypt(message, privateKey):
    """
    @summary: wrapper around rsa.core.decrypt_int function
    @param message: {str} source message
    @param publicKey: {rsa.PrivateKey}
    """
    return _int2bytes(pow(_bytes2int(message), privateKey['d'], privateKey['n']))

def sign(message, privateKey):
    """
    @summary: sign message with private key
    @param message: {str} message to sign
    @param privateKey : {rsa.privateKey} key use to sugn
    """
    return _int2bytes(pow(_bytes2int(message), privateKey['d'], privateKey['n']), (privateKey['n'].bit_length() + 7) // 8)

def verify(message, publicKey):
    """
    @summary: return hash
    @param message: {str} message to verify
    @param publicKey : {rsa.publicKey} key use to sugn
    """
    return _int2bytes(pow(_bytes2int(message), publicKey['e'], publicKey['n']))