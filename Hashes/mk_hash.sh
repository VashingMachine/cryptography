#!/bin/bash
file=personal.txt
md5sum $file | tee -a hash.txt
sha1sum $file | tee -a hash.txt
sha224sum $file | tee -a hash.txt
sha256sum $file | tee -a hash.txt
sha384sum $file | tee -a hash.txt
sha512sum $file | tee -a hash.txt
b2sum $file | tee -a hash.txt
