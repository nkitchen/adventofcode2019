import operator
import os
from collections import namedtuple

DEBUG = os.environ.get("DEBUG")

ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
HALT = 99

Inst = namedtuple('Inst', ['in_param_fns', 'op_fn', 'out_param_fns', 'ip_incr'])

class Computer():
    def run(self, program, inputs):
        self.mem = list(program)
        self.inputs = inputs
        self.outputs = []

        ip = 0
        while True:
            inst = self.decode(ip)

            in_param_fns = [f() for f in inst.in_param_fns]
            try:
                out_param = inst.op_fn(*in_param_fns)
                out_param_fns = [out_param]
            except StopIteration:
                break
            for f, y in zip(inst.out_param_fns, out_param_fns):
                f(y)

            ip += inst.ip_incr

            if DEBUG:
                print(self.mem)

        return self.outputs

    ADDR_MODE = 0
    IMM_MODE = 1

    N_ARGS = {
        ADD: 2,
        MUL: 2,
        INPUT: 0,
        OUTPUT: 1,
    }

    def decode(self, ip):
        code = self.mem[ip]

        op = code % 100
        code //= 100

        n_args = self.N_ARGS.get(op, 0)

        modes = []
        for i in range(n_args):
            modes.append(code % 10)
            code //= 10

        if op == ADD:
            x = self.mem[ip + 1]
            y = self.mem[ip + 2]
            z = self.mem[ip + 3]
            in_param_fns = [
                self.arg_fn(x, modes[0]),
                self.arg_fn(y, modes[1]),
            ]
            op_fn = operator.add
            out_param_fns = [
                self.out_fn(z),
            ]
        elif op == MUL:
            x = self.mem[ip + 1]
            y = self.mem[ip + 2]
            z = self.mem[ip + 3]
            in_param_fns = [
                self.arg_fn(x, modes[0]),
                self.arg_fn(y, modes[1]),
            ]
            op_fn = operator.mul
            out_param_fns = [
                self.out_fn(z),
            ]
        elif op == INPUT:
            z = self.mem[ip + 1]
            in_param_fns = []
            op_fn = self.read_input
            out_param_fns = [
                self.out_fn(z),
            ]
        elif op == OUTPUT:
            x = self.mem[ip + 1]
            in_param_fns = [
                self.arg_fn(x, modes[0]),
            ]
            op_fn = lambda x: x
            out_param_fns = [
                self.write_output,
            ]
        elif op == HALT:
            in_param_fns = []
            out_param_fns = []
            def f():
                raise StopIteration
            op_fn = f
        else:
            raise Exception(f"Unknown opcode: {op}")

        k = len(in_param_fns) + 2
        return Inst(in_param_fns, op_fn, out_param_fns, k)

    def arg_fn(self, a, mode):
        if mode == self.ADDR_MODE:
            def f():
                return self.mem[a]
            return f
        elif mode == self.IMM_MODE:
            def f():
                return a
            return f
        raise Exception(f"Unknown mode: {mode}")

    def out_fn(self, a):
        def f(v):
            self.mem[a] = v
        return f

    def read_input(self):
        x = self.inputs[0]
        self.inputs = self.inputs[1:]
        return x

    def write_output(self, x):
        self.outputs.append(x)
