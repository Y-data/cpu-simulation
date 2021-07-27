'''Models of the hardware components in a CPU'''
from abc import ABC
from typing import NamedTuple, TypeVar
from collections import namedtuple


class BaseHardware(ABC):
    def run(self):
        raise NotImplementedError

T = TypeVar('T', bound='BaseHardware')
AdderOutput = namedtuple('AdderOutput', ['sum', 'carry'])


class Transistor(BaseHardware):
    def __init__(self, state=False):
        self.state = state

    def __str__(self):
        return f'Transistor({self.state})'

    def __repr__(self):
        return f'Transistor({self.state})'

    def set_input(self, state: bool) -> T:
        self.state = state
        return self

    def run(self) -> bool:
        # if state == True than the output is the True
        # if state == False than the output is the False
        return self.state


class ReverseTransistor(Transistor):
    def run(self) -> bool:
        # invert the value
        return not self.state

class NotGate(BaseHardware):
    def __init__(self, input_state=False) -> None:
        self.input_state = input_state
        self.reverse_transistor = ReverseTransistor(input_state)  # only bit of hardware

    def __str__(self):
        return f'NotGate({self.input_state})'

    def __repr__(self):
        return f'NotGate({self.input_state})'

    def update_internals(self) -> None:
        self.reverse_transistor.set_input(self.input_state)

    def set_input(self, input_state: bool) -> T:
        self.input_state = input_state
        self.update_internals()
        return self

    def run(self):
        return self.reverse_transistor.run()


class AndGate(BaseHardware):
    def __init__(self, input_1_state=False, input_2_state=False) -> None:
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.transistor_1 = Transistor(input_1_state)
        self.transistor_2 = Transistor(input_2_state)

    def __str__(self):
        return f'AndGate({self.input_1_state}, {self.input_2_state})'

    def __repr__(self):
        return f'AndGate({self.input_1_state}, {self.input_2_state})'

    def update_internals(self) -> None:
        self.transistor_1.set_input(self.input_1_state)
        self.transistor_2.set_input(self.input_2_state)

    def set_input(self, input_1_state: bool, input_2_state: bool):
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.update_internals()
        return self

    def run(self):
        transistor_state_1 = self.transistor_1.run()
        transistor_state_2 = self.transistor_2.run()
        if transistor_state_1 and transistor_state_2:
            return True
        else:
            return False


class OrGate(BaseHardware):
    def __init__(self, input_1_state=False, input_2_state=False) -> None:
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.transistor_1 = Transistor(input_1_state)
        self.transistor_2 = Transistor(input_2_state)

    def __str__(self):
        return f'OrGate({self.input_1_state}, {self.input_2_state})'

    def __repr__(self):
        return f'OrGate({self.input_1_state}, {self.input_2_state})'

    def update_internals(self) -> None:
        self.transistor_1.set_input(self.input_1_state)
        self.transistor_2.set_input(self.input_2_state)

    def set_input(self, input_1_state: bool, input_2_state: bool):
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.update_internals()
        return self
    
    def run(self):
        transistor_state_1 = self.transistor_1.run()
        transistor_state_2 = self.transistor_2.run()
        if transistor_state_1 or transistor_state_2:
            return True
        else:
            return False


class XOrGate(BaseHardware):
    def __init__(self, input_1_state=False, input_2_state=False) -> None:
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state

        # initialize the logic internally
        self.and_gate_1 = AndGate(input_1_state, input_2_state)  # first and gate
        self.or_gate = OrGate(input_1_state, input_2_state)
        self.not_gate = NotGate(self.and_gate_1.run())  # result from and_gate_1
        self.and_gate_2 = AndGate(self.not_gate.run(), self.or_gate.run())  # first and gate

    def __str__(self):
        return f'OrGate({self.input_1_state}, {self.input_2_state})'

    def __repr__(self):
        return f'OrGate({self.input_1_state}, {self.input_2_state})'

    def update_internals(self):
        '''Updates the internal states by running the parts'''
        self.and_gate_1.set_input(self.input_1_state, self.input_2_state)
        self.or_gate.set_input(self.input_1_state, self.input_2_state)
        self.not_gate.set_input(self.and_gate_1.run())
        self.and_gate_2.set_input(self.not_gate.run(), self.or_gate.run())

    def set_input(self, input_1_state: bool, input_2_state: bool):
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.update_internals()
        return self

    def run(self):
        return self.and_gate_2.run()


class HalfAdder(BaseHardware):
    def __init__(self, input_1_state=False, input_2_state=False) -> None:
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state

        # initialize the logic internally
        self.xor_gate = XOrGate(input_1_state, input_2_state)
        self.and_gate = AndGate(input_1_state, input_2_state)

    def __str__(self):
        return f'HalfAdder({self.input_1_state}, {self.input_2_state})'

    def __repr__(self):
        return f'HalfAdder({self.input_1_state}, {self.input_2_state})'

    def update_internals(self):
        self.xor_gate.set_input(self.input_1_state, self.input_2_state)
        self.and_gate.set_input(self.input_1_state, self.input_2_state)

    def set_input(self, input_1_state: bool, input_2_state: bool):
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.update_internals()
        return self

    def run(self):
        output_sum = self.xor_gate.run()
        output_carry = self.and_gate.run()

        return AdderOutput(sum=output_sum, carry=output_carry)


class FullAdder(BaseHardware):
    def __init__(self, input_1_state=False, input_2_state=False, input_3_state=False) -> None:
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.input_3_state = input_3_state

        # initialize the logic internally
        self.half_adder_1 = HalfAdder(input_1_state, input_2_state)
        half_adder_1_output = self.half_adder_1.run()

        self.half_adder_2 = HalfAdder(half_adder_1_output.sum, input_3_state)
        half_adder_2_output = self.half_adder_2.run()

        self.or_gate = OrGate(half_adder_1_output.carry, half_adder_2_output.carry)

    def __str__(self):
        return f'FullAdder({self.input_1_state}, {self.input_2_state}, {self.input_3_state})'

    def __repr__(self):
        return f'FullAdder({self.input_1_state}, {self.input_2_state}, {self.input_3_state})'

    def update_internals(self):
        self.half_adder_1.set_input(self.input_1_state, self.input_2_state)
        half_adder_1_output = self.half_adder_1.run()

        self.half_adder_2.set_input(half_adder_1_output.sum, self.input_3_state)
        half_adder_2_output = self.half_adder_2.run()

        self.or_gate.set_input(half_adder_1_output.carry, half_adder_2_output.carry)

    def set_input(self, input_1_state: bool, input_2_state: bool, input_3_state: bool):
        self.input_1_state = input_1_state
        self.input_2_state = input_2_state
        self.input_3_state = input_3_state
        self.update_internals()
        return self

    def run(self):
        output_carry = self.or_gate.run()
        half_adder_2_output = self.half_adder_2.run()

        return AdderOutput(sum=half_adder_2_output.sum, carry=output_carry)
    