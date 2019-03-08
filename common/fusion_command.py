from wpilib.command import Command, CommandGroup, InstantCommand, Subsystem

import robotmap


class FusionCommand(Command):
    """
    A class that implements `control_mode` checking. It will automatically end if it detects
    the operator has left the desired control_mode.
    """

    def __init__(self, name, control_mode, sub=None):
        """
        `__init__` takes three arguments: `name` is the name of your command, 
        `control_mode` is the desired control_mode for it to operate in, and 
        `sub` (default `None`) is the subsystem it requires
        """
        super().__init__(name + str(control_mode), subsystem=sub)
        self.control_mode = control_mode

    def initialize(self):
        if robotmap.control_mode is self.control_mode:
            pass
        else:
            self.end()

    def execute(self):
        if robotmap.control_mode is self.control_mode:
            pass
        else:
            self.end()

    def interrupted(self):
        self.end()


class FusionInstantCommand(InstantCommand):
    def __init__(self, name, control_mode, sub=None):
        super().__init__(name + str(control_mode), subsystem=sub)
        self.control_mode = control_mode

    def initialize(self):
        if robotmap.control_mode is self.control_mode:
            pass
        else:
            self.end()


# TODO

# class FusionCommandGroup(CommandGroup):
#     def __init__(self, name, control_mode, sub=None):
#         super().__init__(name + str(control_mode), subsystem=sub)
#         self.control_mode = control_mode

#     def initialize(self):
#         if robotmap.control_mode is self.control_mode:
#             pass
#         else:
#             self.end()

#     def execute(self):
#         if robotmap.control_mode is self.control_mode:
#             pass
#         else:
#             self.end()

#     def interrupted(self):
#         self.end()
