import multiprocessing as mp
import operator
import os
import sys
from collections import namedtuple
from enum import IntEnum

DEBUG = os.environ.get("DEBUG")

class Op(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JMPT = 5
    JMPF = 6
    LT = 7
    EQ = 8
    HALT = 99

class Mode(IntEnum):
    ADDR = 0
    IMM = 1

N_ARGS = {
    Op.ADD: 2,
    Op.MUL: 2,
    Op.INPUT: 0,
    Op.OUTPUT: 1,
    Op.JMPT: 2,
    Op.JMPF: 2,
    Op.LT: 2,
    Op.EQ: 2,
}

class Process():
    def __init__(self, program, input_queue=None, output_queue=None):
        self.mem = list(program)

        if input_queue is None:
            self.input_queue = mp.SimpleQueue()
        else:
            self.input_queue = input_queue

        if output_queue is None:
            self.output_queue = mp.SimpleQueue()
        else:
            self.output_queue = output_queue

        self._proc = mp.Process(target=self.run, daemon=True)
        self._proc.start()

    def run(self):
        self.ip = 0
        while True:
            if DEBUG:
                self.dump()

            inst = self.decode(self.ip)

            args = [self.load_arg(p) for p in inst.src_params]
            try:
                ret_values, next_ip = self.exec(inst, args)
            except StopIteration:
                self.output_queue.put(None)
                break

            for rv, p in zip(ret_values, inst.dst_params):
                self.store(rv, p)

            if next_ip is None:
                self.ip += inst.ip_incr()
            else:
                self.ip = next_ip

    def decode(self, ip):
        code = self.mem[ip]

        op = code % 100
        try:
            op = Op(op)
        except ValueError:
            pass
        code //= 100

        n_args = N_ARGS.get(op, 0)

        modes = []
        for i in range(n_args):
            modes.append(code % 10)
            code //= 10

        # Unrecognized mode?  Keep it undecoded.
        if not(set(modes) <= set([Mode.ADDR, Mode.IMM])):
            op = code

        if ip + n_args >= len(self.mem):
            # Op without args -- keep it undecoded.
            src_params = []
            dst_params = []
        elif op in [Op.ADD, Op.MUL, Op.LT, Op.EQ]:
            x = self.mem[ip + 1]
            y = self.mem[ip + 2]
            z = self.mem[ip + 3]
            src_params = [
                Param(x, modes[0]),
                Param(y, modes[1]),
            ]
            dst_params = [
                Param(z, Mode.ADDR),
            ]
        elif op == Op.INPUT:
            z = self.mem[ip + 1]
            src_params = []
            dst_params = [
                Param(z, Mode.ADDR),
            ]
        elif op == Op.OUTPUT:
            x = self.mem[ip + 1]
            src_params = [
                Param(x, modes[0]),
            ]
            dst_params = []
        elif op in [Op.JMPT, Op.JMPF]:
            x = self.mem[ip + 1]
            y = self.mem[ip + 2]
            src_params = [
                Param(x, modes[0]),
                Param(y, modes[1]),
            ]
            dst_params = []
        else:
            src_params = []
            dst_params = []

        return Inst(op, src_params, dst_params)

    def load_arg(self, param):
        if param.mode == Mode.IMM:
            return param.num
        else:
            assert param.mode == Mode.ADDR
            return self.mem[param.num]

    def store(self, value, param):
        assert param.mode == Mode.ADDR
        self.mem[param.num] = value

    def exec(self, inst, args):
        r = None
        next_ip = None
        if inst.op == Op.ADD:
            r = args[0] + args[1]
        elif inst.op == Op.MUL:
            r = args[0] * args[1]
        elif inst.op == Op.INPUT:
            r = self.input_queue.get()
        elif inst.op == Op.OUTPUT:
            self.output_queue.put(args[0])
        elif inst.op == Op.JMPT:
            if args[0] != 0:
                next_ip = args[1]
        elif inst.op == Op.JMPF:
            if args[0] == 0:
                next_ip = args[1]
        elif inst.op == Op.LT:
            r = int(args[0] < args[1])
        elif inst.op == Op.EQ:
            r = int(args[0] == args[1])
        elif inst.op == Op.HALT:
            raise StopIteration
        else:
            raise Exception(f"Unknown opcode: {inst.op}")

        ret_values = []
        if r is not None:
            ret_values.append(r)

        return ret_values, next_ip

    def read(self):
        return self.output_queue.get()

    def read_all(self):
        while True:
            value = self.read()
            if value is None:
                return
            yield value

    def write(self, value):
        self.input_queue.put(value)

    def dump(self):
        def write(s):
            print(s, file=sys.stderr, end='')

        ip = 0
        while ip < len(self.mem):
            if ip == self.ip:
                write("==> ")
            else:
                write("    ")

            write(f" [{ip:0>3d}] ")

            inst = self.decode(ip)

            # 20 columns for 1-4 memory values
            m = ""
            for i in range(ip, ip + inst.ip_incr()):
                m += f"{self.mem[i]:4d} "
            write(f"{m:20}")

            write(str(inst) + "\n")

            ip += inst.ip_incr()
        write("\n")

class Param(namedtuple('Param', 'num mode')):
    def __str__(self):
        if self.mode == Mode.ADDR:
            return f"[{self.num}]"
        else:
            assert self.mode == Mode.IMM
            return f"#{self.num}"

class Inst(namedtuple('Inst', ['op', 'src_params', 'dst_params'])):
    def __str__(self):
        if isinstance(self.op, Op):
            s = self.op.name
        else:
            s = f"{self.op}!"
        if self.src_params:
            s += ' ' + ', '.join(str(a) for a in self.src_params)
        if self.dst_params:
            s += ' > ' + ', '.join(str(r) for r in self.dst_params)
        return s

    def ip_incr(self):
        return 1 + len(self.src_params) + len(self.dst_params)
