#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import *
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    truth_table_test = [(True, True), (True, False), (False, True), (False, False)]
    truth_table_test_three = [
        (True, True, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
        (True, False, False),
        (False, False, True),
        (False, True, False),
        (False, False, False)]
    and_gate = AndGate()
    or_gate = OrGate()
    xor_gate = XOrGate()
    half_adder = HalfAdder()
    full_adder = FullAdder()

    logging.debug('Testing AndGate')
    for (v1, v2) in truth_table_test:
        logging.debug(f'{v1} {v2} {and_gate.set_input(v1, v2).run()}')

    print()

    logging.debug('Testing OrGate')
    for (v1, v2) in truth_table_test:
        logging.debug(f'{v1} {v2} {or_gate.set_input(v1, v2).run()}')

    print()

    logging.debug('Testing XOrGate')
    for (v1, v2) in truth_table_test:
        logging.debug(f'{v1} {v2} {xor_gate.set_input(v1, v2).run()}')

    print()
    logging.debug('Testing HalfAdder')
    for (v1, v2) in truth_table_test:
        logging.debug(f'{int(v1)} + {int(v2)} = {int(half_adder.set_input(v1, v2).run().carry)}{int(half_adder.set_input(v1, v2).run().sum)}')

    print()
    logging.debug('Testing FullAdder')
    for (v1, v2, v3) in truth_table_test_three:
        logging.debug(f'{int(v1)} + {int(v2)} + {int(v3)} = {int(full_adder.set_input(v1, v2, v3).run().carry)}{int(full_adder.set_input(v1, v2, v3).run().sum)}')
