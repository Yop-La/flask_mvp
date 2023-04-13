from pyramid.config import Configurator

config = Configurator()
config.scan('app')

import sys
sys.path.append('..')
