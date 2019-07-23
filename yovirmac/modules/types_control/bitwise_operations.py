"""Байтовые операции"""
from yovirmac.modules.constants import *


def bitwise_not(num):
    """Битовое НЕ"""
    global memory
    memory[num] = ~memory[num] & full_cell


def bitwise_and(num, mask):
    """Битовое И"""
    global memory
    memory[num] = memory[num] & mask


def bitwise_or(num, mask):
    """Битовое ИЛИ"""
    global memory
    memory[num] = memory[num] | mask


def bitwise_xor(num, mask):
    """Битовое ЛИБО"""
    global memory
    memory[num] = memory[num] ^ mask
