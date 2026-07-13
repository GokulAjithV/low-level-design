from abc import ABC, abstractmethod

# =====================================================================
# CHALLENGE: Smart Home Automation Remote Control
# =====================================================================

# 1. Receivers (Smart Devices)
class Light:
    def __init__(self):
        self.is_on = False

    def turn_on(self) -> None:
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False


class Stereo:
    def __init__(self):
        self.volume = 10  # Default volume

    def set_volume(self, level: int) -> None:
        self.volume = level


# 2. Command Interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


# 3. Concrete Commands
# TODO: Implement LightOnCommand
class LightOnCommand(Command):
    def __init__(self, light: Light):
        # TODO: Store reference to light receiver
        pass

    def execute(self) -> None:
        # TODO: Turn the light on
        pass

    def undo(self) -> None:
        # TODO: Undo action (turn the light off)
        pass


# TODO: Implement LightOffCommand
class LightOffCommand(Command):
    def __init__(self, light: Light):
        # TODO: Store reference to light receiver
        pass

    def execute(self) -> None:
        # TODO: Turn the light off
        pass

    def undo(self) -> None:
        # TODO: Undo action (turn the light on)
        pass


# TODO: Implement StereoVolumeCommand
class StereoVolumeCommand(Command):
    def __init__(self, stereo: Stereo, volume: int):
        # TODO: Store reference to stereo, target volume, and track previous volume
        pass

    def execute(self) -> None:
        # TODO: Store current volume as previous volume, then set new volume
        pass

    def undo(self) -> None:
        # TODO: Restore previous volume
        pass


# 4. Invoker (RemoteControl)
class RemoteControl:
    def __init__(self):
        # TODO: Initialize undo and redo stacks
        pass

    def press_button(self, command: Command) -> None:
        # TODO: Execute command, push to undo stack, and CLEAR redo stack
        pass

    def press_undo(self) -> None:
        # TODO: Pop from undo stack, undo it, and push it to redo stack
        pass

    def press_redo(self) -> None:
        # TODO: Pop from redo stack, execute it, and push it to undo stack
        pass


# =====================================================================
# CLIENT / VERIFICATION CODE (Do not modify this part)
# =====================================================================

def verify_command():
    print("--- Testing Command (Smart Remote Control) ---")
    
    # Receivers
    living_room_light = Light()
    living_room_stereo = Stereo()
    
    # Invoker
    remote = RemoteControl()
    
    # 1. Turn Light On
    print("Pressing: Turn Light On")
    remote.press_button(LightOnCommand(living_room_light))
    
    # 2. Adjust Stereo Volume to 25
    print("Pressing: Set Volume to 25")
    remote.press_button(StereoVolumeCommand(living_room_stereo, 25))
    
    # 3. Adjust Stereo Volume to 40
    print("Pressing: Set Volume to 40")
    remote.press_button(StereoVolumeCommand(living_room_stereo, 40))
    
    try:
        assert living_room_light.is_on is True, "❌ Failed: Light should be on"
        assert living_room_stereo.volume == 40, f"❌ Failed: Volume should be 40. Got: {living_room_stereo.volume}"
        print("✅ Command execution: Success!")
        
        # 4. Test Undo 1 (Stereo volume back to 25)
        print("Undoing volume adjustment to 40...")
        remote.press_undo()
        assert living_room_stereo.volume == 25, f"❌ Failed: Volume should have undone back to 25. Got: {living_room_stereo.volume}"
        
        # 5. Test Undo 2 (Stereo volume back to 10)
        print("Undoing volume adjustment to 25...")
        remote.press_undo()
        assert living_room_stereo.volume == 10, f"❌ Failed: Volume should have undone back to default 10. Got: {living_room_stereo.volume}"
        
        # 6. Test Redo 1 (Stereo volume back to 25)
        print("Redoing volume adjustment to 25...")
        remote.press_redo()
        assert living_room_stereo.volume == 25, f"❌ Failed: Redo volume should be 25. Got: {living_room_stereo.volume}"
        
        # 7. Test Redo 2 (Stereo volume back to 40)
        print("Redoing volume adjustment to 40...")
        remote.press_redo()
        assert living_room_stereo.volume == 40, f"❌ Failed: Redo volume should be 40. Got: {living_room_stereo.volume}"
        
        # 8. Test Redo clearing on new command
        print("Undoing volume adjustment to 40...")
        remote.press_undo() # Undo to 25. Redo stack now contains the volume 40 command.
        
        print("Pressing: Turn Light Off")
        remote.press_button(LightOffCommand(living_room_light)) # New command. Redo stack must clear.
        
        print("Attempting Redo (should do nothing)...")
        remote.press_redo()
        assert living_room_light.is_on is False, "❌ Failed: Light should remain Off"
        assert living_room_stereo.volume == 25, f"❌ Failed: Redo stack should have cleared, leaving volume at 25. Got: {living_room_stereo.volume}"
        
        print("✅ Undo / Redo functionality: Success!")
        print("\n✅ Command Challenge: Success!")
    except AssertionError as e:
        print(f"\n❌ Assertion Failed: {e}")
    except Exception as e:
        print(f"\n❌ Failed with unexpected error: {e}")


if __name__ == "__main__":
    verify_command()
