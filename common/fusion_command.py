from wpilib.command import Command, CommandGroup, InstantCommand

import robotmap


class FusionCommand(Command):
    def __init__(self, name, control_mode, sub=None):
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


# DEPRECATED

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
