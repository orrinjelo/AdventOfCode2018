#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit


class VirtualMachine(object):
    def __init__(self, reg=[0, 0, 0, 0, 0, 0]):
        self.__registers = reg

        self.__ip = None
        self.__pc = 0

        self.instructions = []

        self.ops = {
            0: self.banr,
            1: self.addr,
            2: self.eqri,
            3: self.setr,
            4: self.gtrr,
            5: self.bori,
            6: self.gtir,
            7: self.seti,
            8: self.borr,
            9: self.bani,
            10: self.eqir,
            11: self.eqrr,
            12: self.gtri,
            13: self.addi,
            14: self.muli,
            15: self.mulr,

            16: self.addr,
            17: self.addi,
            18: self.mulr,
            19: self.muli,
            20: self.banr,
            21: self.bani,
            22: self.borr,
            23: self.bori,
            24: self.setr,
            25: self.seti,
            26: self.gtir,
            27: self.gtri,
            28: self.gtrr,
            29: self.eqir,
            30: self.eqri,
            31: self.eqrr,            

            'addr': self.addr,
            'addi': self.addi,
            'mulr': self.mulr,
            'muli': self.muli,
            'banr': self.banr,
            'bani': self.bani,
            'borr': self.borr,
            'bori': self.bori,
            'setr': self.setr,
            'seti': self.seti,
            'gtir': self.gtir,
            'gtri': self.gtri,
            'gtrr': self.gtrr,
            'eqir': self.eqir,
            'eqri': self.eqri,
            'eqrr': self.eqrr,
            '#ip': self.setip,            
        }

    @property
    def registers(self):
        return self.__registers
    
    @property
    def ip(self):
        return self.__ip
    

    def addr(self, A, B, C):
        self.__registers[C] = self.registers[A] + self.registers[B]

    def addi(self, A, B, C):
        self.__registers[C] = self.registers[A] + B

    def mulr(self, A, B, C):
        self.__registers[C] = self.registers[A] * self.registers[B]

    def muli(self, A, B, C):
        self.__registers[C] = self.registers[A] * B

    def banr(self, A, B, C):
        self.__registers[C] = self.registers[A] & self.registers[B]

    def bani(self, A, B, C):
        self.__registers[C] = self.registers[A] & B

    def borr(self, A, B, C):
        self.__registers[C] = self.registers[A] | self.registers[B]

    def bori(self, A, B, C):
        self.__registers[C] = self.registers[A] | B

    def setr(self, A, B, C):
        self.__registers[C] = self.registers[A]

    def seti(self, A, B, C):
        self.__registers[C] = A

    def gtir(self, A, B, C):
        self.__registers[C] = 1 if A > self.registers[B] else 0

    def gtri(self, A, B, C):
        self.__registers[C] = 1 if self.registers[A] > B else 0

    def gtrr(self, A, B, C):
        self.__registers[C] = 1 if self.registers[A] > self.registers[B] else 0

    def eqir(self, A, B, C):
        self.__registers[C] = 1 if A == self.registers[B] else 0

    def eqri(self, A, B, C):
        self.__registers[C] = 1 if self.registers[A] == B else 0

    def eqrr(self, A, B, C):
        self.__registers[C] = 1 if self.registers[A] == self.registers[B] else 0

    def setip(self, A, B, C):
        last = self.registers[self.__ip if self.__ip is not None else self.__pc]
        self.__ip = A
        try:
            del self.instructions[last]
        except:
            pass

    def load(self, lines):
        ins = re.compile(r'(#?[A-Za-z]+)\s+(\d+)\s*(\d*)\s*(\d*)')
        for l in lines:
            c = ins.match(l)
            instr  = c.groups(1)[0]
            if instr == '#ip':
                A, B, C = int(c.groups(1)[1]),0,0
            else:
                A, B, C = int(c.groups(1)[1]),int(c.groups(1)[2]),int(c.groups(1)[3])
            self.instructions.append([instr,A,B,C])

    def exec_once(self, inst=None):
        if inst is not None:
            op, A, B, C = inst
        else:
            op, A, B, C = self.instructions[self.registers[self.__ip] if self.__ip is not None else self.__pc]
        # print(op, A, B, C)
        if not op in self.ops.keys():
            raise ValueError(f'Invalid op code: {op} ({inst})')
        self.ops[op](A, B, C)
        if self.__ip is not None and op != '#ip':
            self.__registers[self.__ip] += 1
        self.__pc += 1

    def exec(self):
        while (self.registers[self.__ip] if self.__ip is not None else self.__pc) < len(self.instructions):
            print(self.registers)
            self.exec_once()

class VMTests:
    @staticmethod
    def run_tests():
        VMTests.test_addr()
        VMTests.test_addi()
        VMTests.test_mulr()
        VMTests.test_muli()
        VMTests.test_banr()
        VMTests.test_bani()
        VMTests.test_borr()
        VMTests.test_bori()
        VMTests.test_setr()
        VMTests.test_seti()
        VMTests.test_gtir()
        VMTests.test_gtri()
        VMTests.test_gtrr()
        VMTests.test_eqir()
        VMTests.test_eqri()
        VMTests.test_eqrr()
        VMTests.test_s_ip()
        print('All tests executed successfully.')

    @staticmethod
    def test_addr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([16, 0, 1, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec_once([16, 0, 2, 3])
        assert(vm.registers == [1,2,3,4])
        vm.exec_once([16, 1, 2, 3])
        assert(vm.registers == [1,2,3,5])
        vm.exec_once([16, 2, 3, 0])
        assert(vm.registers == [8,2,3,5])
        vm.exec_once([16, 0, 0, 0])
        assert(vm.registers == [16,2,3,5])

    @staticmethod
    def test_addi():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([17, 0, 1, 3])
        assert(vm.registers == [1,2,3,2])
        vm.exec_once([17, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec_once([17, 1, 2, 3])
        assert(vm.registers == [1,2,3,4])
        vm.exec_once([17, 2, 3, 0])
        assert(vm.registers == [6,2,3,4])
        vm.exec_once([17, 0, 0, 0])
        assert(vm.registers == [6,2,3,4])
        vm.exec_once([17, 0, -6, 0])
        assert(vm.registers == [0,2,3,4])

    @staticmethod
    def test_mulr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([18, 0, 1, 3])
        assert(vm.registers == [1,2,3,2])
        vm.exec_once([18, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec_once([18, 1, 2, 3])
        assert(vm.registers == [1,2,3,6])
        vm.exec_once([18, 2, 3, 0])
        assert(vm.registers == [18,2,3,6])
        vm.exec_once([18, 0, 0, 0])
        assert(vm.registers == [18*18,2,3,6])

    @staticmethod
    def test_muli():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([19, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec_once([19, 0, 2, 3])
        assert(vm.registers == [1,2,3,2])
        vm.exec_once([19, 1, 2, 3])
        assert(vm.registers == [1,2,3,4])
        vm.exec_once([19, 2, 3, 0])
        assert(vm.registers == [9,2,3,4])
        vm.exec_once([19, 0, 0, 0])
        assert(vm.registers == [0,2,3,4])

    @staticmethod
    def test_banr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([20, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([20, 0, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_bani():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([21, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec_once([21, 0, 2, 3])
        assert(vm.registers == [1,2,3,0])

    @staticmethod
    def test_borr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([22, 0, 1, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec_once([22, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])

    @staticmethod
    def test_bori():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([23, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec_once([23, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])

    @staticmethod
    def test_setr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([24, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_seti():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([25, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])

    @staticmethod
    def test_gtir():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([26, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([26, 4, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_gtri():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([27, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([27, 2, 2, 3])
        assert(vm.registers == [1,2,3,1])


    @staticmethod
    def test_gtrr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([28, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([28, 1, 2, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([28, 2, 3, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_eqir():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([29, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([29, 3, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_eqri():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([30, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec_once([30, 2, 2, 3])
        assert(vm.registers == [1,2,3,0])

    @staticmethod
    def test_eqrr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec_once([31, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([31, 1, 2, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec_once([31, 2, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_s_ip():
        vm = VirtualMachine([0, 0, 0, 0])
        vm.exec_once(['#ip', 0, 0, 0])
        vm.exec_once(['seti', 2, 0, 0])
        assert(vm.registers == [3, 0, 0, 0])

if __name__ == '__main__':
    VMTests.run_tests()

    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')


    vm = VirtualMachine()

    vm.load(lines)
    vm.exec()

    pprint(vm.registers)
