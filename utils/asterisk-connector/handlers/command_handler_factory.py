from command_handlers import Asterisk10CommandHandler
from command_handlers import Asterisk11CommandHandler
from command_handlers import Queue16CommandHandler

from command_constants import Protocol

class CommandHandlerFactory:
    """Command handler factory"""
    
    @staticmethod
    def create_command_handler_by_protocol(protocol_version):
        """Create concrete command handler based on command protocol"""
        
        if protocol_version == Protocol.ASTERISK_1_0:
            return Asterisk10CommandHandler()

        elif protocol_version == Protocol.ASTERISK_1_1:
            return Asterisk11CommandHandler()

    @staticmethod
    def create_command_handler_by_key(key):
        """Create concrete command handler based on command protocol"""

        if key in Protocol.versions():
            return CommandHandlerFactory.create_command_handler_by_protocol(key)

        elif key == Protocol.QUEUE_1_6:
            return Queue16CommandHandler()
