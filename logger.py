""" Custom logger. """

import logging

def new():
    """Sets custom formatting and returns a logger"""
    logging.basicConfig(format='%(levelname)s:%(filename)s:Ln%(lineno)s: %(message)s', level=logging.DEBUG)
    return logging.getLogger()
