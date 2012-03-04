import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from asterisk_1_0_command_handler import Asterisk10CommandHandler
from asterisk_1_1_command_handler import Asterisk11CommandHandler
from queue_1_6_command_handler import Queue16CommandHandler

