from __future__ import annotations
from distutils import command

from typing import TYPE_CHECKING, Any

from .command import Command

if TYPE_CHECKING:
    from .client import CommandsClient

__all__ = ("Cog", "CogMeta")

class CogMeta(type):
    _commands: list[Command]

    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        commands: list[Command] = []
        self = super().__new__(cls, name, bases, attrs)

        for base in reversed(self.__mro__):
            for value in base.__dict__.values():
                if isinstance(value, Command):
                    value.cog = self  # type: ignore
                    commands.append(value)


        self._commands = commands

        return self

class Cog(metaclass=CogMeta):
    _commands: list[Command]

    def _inject(self, client: CommandsClient):
        client.cogs[type(self).__name__] = self

        for command in self._commands:
            client.add_command(command.name, command)

    def _uninject(self, client: CommandsClient):
        for name, command in client.all_commands.copy().items():
            if command in self._commands:
                del client.all_commands[name]
