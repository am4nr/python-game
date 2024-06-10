from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.Character.character import Character
from scripts.Character.characterState import (
    RunningRight,
    RunningLeft,
    Jumping,
    Idle,
)
from scripts.Character.characterMovement import HorizontalMovement, VerticalMovement
from scripts.Utils.settings import *


class PlayerCommand:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def execute(self, character: "Character"):
        raise NotImplementedError


class NoInput(PlayerCommand):
    def execute(self, character: "Character"):
        if (
            character.on_ground
            and not character.hit
            and character.state.currentState != Idle
        ):
            character.idle_waiting_time_counter += 1
            if character.idle_waiting_time_counter >= 12:
                character.state.changeState(Idle)


class RunLeft(PlayerCommand):
    def execute(self, character: "Character"):
        if character.on_ground and not character.hit:
            character.state.changeState(RunningLeft)
        HorizontalMovement().execute(character)


class RunRight(PlayerCommand):
    def execute(self, character: "Character"):
        if character.on_ground and not character.hit:
            character.state.changeState(RunningRight)
        HorizontalMovement().execute(character)


class Jump(PlayerCommand):
    def execute(self, character: "Character"):
        if not character.hit:
            character.state.changeState(Jumping)
            VerticalMovement().execute(character)
