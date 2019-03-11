#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2018/12/6
@author: shimakaze-git
'''


class Blockchain:

    """ Blockchain class constructor"""
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.transaction_index = 0

    """ create block in blockchain """
    def create_block(self, nonce, previous_hash):
        pass

    """ create transaction in blockchain """
    def create_transaction(self, sender, recipient, amount):
        pass

    """ valid current chain """
    def create_node(self, node):
        pass

    """ calid chain """
    def valid_chain(self, chain):
        pass

    """ consensus algorithm """
    def resolve_conflicts(self, block_list):
        pass

blockchain = Blockchain()
blockchain.chain