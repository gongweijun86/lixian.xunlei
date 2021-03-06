# -*- encoding: utf-8 -*-
# binux<17175297.hk@gmail.com>

import os
import struct
import hashlib

def parse_fid(fid):
    cid, size, gcid = struct.unpack("<20sq20s", fid.decode("base64"))
    return cid.encode("hex").upper(), size, gcid.encode("hex").upper()

def gen_fid(cid, size, gcid):
    return struct.pack("<20sq20s", cid.decode("hex"), size, gcid.decode("hex")).encode("base64").replace("\n", "")

def gcid_hash_file(path):
    h = hashlib.sha1()
    size = os.path.getsize(path)
    psize = 0x40000
    while size / psize > 0x200:
        psize = psize << 1
    with open(path, 'rb') as stream:
        data = stream.read(psize)
        while data:
            h.update(hashlib.sha1(data).digest())
            data = stream.read(psize)
    return h.hexdigest().upper()

def cid_hash_file(path):
    h = hashlib.sha1()
    size = os.path.getsize(path)
    with open(path, 'rb') as stream:
        if size < 0xF000:
            h.update(stream.read())
        else:
            h.update(stream.read(0x5000))
            stream.seek(size/3)
            h.update(stream.read(0x5000))
            stream.seek(size-0x5000)
            h.update(stream.read(0x5000))
    return h.hexdigest().upper()

def encode_thunder(url):
    return "thunder://"+("AA"+url+"ZZ").encode("base64").replace("\n", "")
