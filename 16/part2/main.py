#!/usr/bin/env python3
import os, sys
import numpy as np 
from pprint import pprint
import time
import re

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from utils.timeit import timeit


class VirtualMachine(object):
    def __init__(self, reg=[0, 0, 0, 0]):
        self.__registers = reg

        self.ops = {
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
        }

    @property
    def registers(self):
        return self.__registers
    

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

    def exec(self, inst):
        op, A, B, C = inst
        if not op in self.ops.keys():
            raise ValueError('Invalid op code')
        self.ops[op](A, B, C)

    def train(self, inst, before, result):
        ok = []
        self.backup = self.registers[:]
        for op in range(16,32):
            self.__registers = before[:]
            self.ops[op](inst[1], inst[2], inst[3])
            if self.registers == result:
                ok.append(op)

        # print(ok)
        if len(ok) == 1:
            self.ops[inst[0]] = self.ops[ok[0]]
        else:
            if inst[0] not in self.ops.keys():
                self.ops[inst[0]] = ok
            else:
                new_ok = []
                if type(self.ops[inst[0]]) == list:
                    for o in ok:
                        if o in self.ops[inst[0]]:
                            try:
                                if type(self.ops[o]) != list:
                                    continue
                            except:
                                pass
                            new_ok.append(o)
                    if len(new_ok) == 1:
                        self.ops[inst[0]] = new_ok[1]

        # Fix os
        for op in range(16):
            try:
                if type(self.ops[op]) == list:
                    for e in self.ops[op]:
                        try:
                            if type(self.ops[e-16]) != list:
                                self.ops[op].remove(e)
                        except:
                            pass
                    if len(self.ops[op]) == 1:
                        self.ops[op] = self.ops[self.ops[op][0]]
            except:
                pass

        self.__registers = self.backup[:]
        return ok

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
        print('All tests executed successfully.')

    @staticmethod
    def test_addr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([16, 0, 1, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec([16, 0, 2, 3])
        assert(vm.registers == [1,2,3,4])
        vm.exec([16, 1, 2, 3])
        assert(vm.registers == [1,2,3,5])
        vm.exec([16, 2, 3, 0])
        assert(vm.registers == [8,2,3,5])
        vm.exec([16, 0, 0, 0])
        assert(vm.registers == [16,2,3,5])

    @staticmethod
    def test_addi():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([17, 0, 1, 3])
        assert(vm.registers == [1,2,3,2])
        vm.exec([17, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec([17, 1, 2, 3])
        assert(vm.registers == [1,2,3,4])
        vm.exec([17, 2, 3, 0])
        assert(vm.registers == [6,2,3,4])
        vm.exec([17, 0, 0, 0])
        assert(vm.registers == [6,2,3,4])
        vm.exec([17, 0, -6, 0])
        assert(vm.registers == [0,2,3,4])

    @staticmethod
    def test_mulr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([18, 0, 1, 3])
        assert(vm.registers == [1,2,3,2])
        vm.exec([18, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec([18, 1, 2, 3])
        assert(vm.registers == [1,2,3,6])
        vm.exec([18, 2, 3, 0])
        assert(vm.registers == [18,2,3,6])
        vm.exec([18, 0, 0, 0])
        assert(vm.registers == [18*18,2,3,6])

    @staticmethod
    def test_muli():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([19, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec([19, 0, 2, 3])
        assert(vm.registers == [1,2,3,2])
        vm.exec([19, 1, 2, 3])
        assert(vm.registers == [1,2,3,4])
        vm.exec([19, 2, 3, 0])
        assert(vm.registers == [9,2,3,4])
        vm.exec([19, 0, 0, 0])
        assert(vm.registers == [0,2,3,4])

    @staticmethod
    def test_banr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([20, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([20, 0, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_bani():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([21, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec([21, 0, 2, 3])
        assert(vm.registers == [1,2,3,0])

    @staticmethod
    def test_borr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([22, 0, 1, 3])
        assert(vm.registers == [1,2,3,3])
        vm.exec([22, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])

    @staticmethod
    def test_bori():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([23, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec([23, 0, 2, 3])
        assert(vm.registers == [1,2,3,3])

    @staticmethod
    def test_setr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([24, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_seti():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([25, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])

    @staticmethod
    def test_gtir():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([26, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([26, 4, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_gtri():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([27, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([27, 2, 2, 3])
        assert(vm.registers == [1,2,3,1])


    @staticmethod
    def test_gtrr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([28, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([28, 1, 2, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([28, 2, 3, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_eqir():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([29, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([29, 3, 2, 3])
        assert(vm.registers == [1,2,3,1])

    @staticmethod
    def test_eqri():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([30, 0, 1, 3])
        assert(vm.registers == [1,2,3,1])
        vm.exec([30, 2, 2, 3])
        assert(vm.registers == [1,2,3,0])


    @staticmethod
    def test_eqrr():
        vm = VirtualMachine([1,2,3,0])
        vm.exec([31, 0, 1, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([31, 1, 2, 3])
        assert(vm.registers == [1,2,3,0])
        vm.exec([31, 2, 2, 3])
        assert(vm.registers == [1,2,3,1])

if __name__ == '__main__':
    VMTests.run_tests()

    if len(sys.argv) <= 1:
        sys.exit('No entries given.  Answer: unknown')

    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        sys.exit('Too many args.')

    bre = re.compile(r'Before: \[(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\]')
    are = re.compile(r'After:  \[(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\]')
    ins = re.compile(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')

    count = 0

    vm = VirtualMachine()

    for i in range(0,len(lines),4):
        b = bre.match(lines[i])
        c = ins.match(lines[i+1])
        a = are.match(lines[i+2])

        before = [int(b.groups(1)[0]),int(b.groups(1)[1]),int(b.groups(1)[2]),int(b.groups(1)[3])]
        instr  = [int(c.groups(1)[0]),int(c.groups(1)[1]),int(c.groups(1)[2]),int(c.groups(1)[3])]
        after  = [int(a.groups(1)[0]),int(a.groups(1)[1]),int(a.groups(1)[2]),int(a.groups(1)[3])]

        results = vm.train(instr, before, after)

        if len(results) >= 3:
            count += 1
    pprint(vm.ops)

    print(f'Answer: {count}/{len(lines)//4}')