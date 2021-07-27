#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import *
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    truth_table_test = [(True, True), (True, False), (False, True), (False, False)]
    and_gate = AndGate()
    or_gate = OrGate()
    xor_gate = XOrGate()

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