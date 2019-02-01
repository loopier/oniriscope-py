import logging

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s:%(filename)s:Ln%(lineno)s: %(message)s', level=logging.DEBUG)
log = logging.getLogger()
