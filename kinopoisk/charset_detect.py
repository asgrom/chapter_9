"""Определение кодировки файла"""
import chardet


def chaset_detect(filename):
    with open(filename, 'rb') as f:
        charset = chardet.detect(f.read())['encoding']
    return charset
