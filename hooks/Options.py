# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#

class GoalCondition(Choice):
    """Choose your win condition. Shuttle Clear: Finish Shuttle Clear. Gold Standard: Gold every level on Earth and the Moon. Solar System: Gold every level in the solar system (Earth, Moon, Mercury, Venus, Mars, Neptune). Gold Time Attack: Gold on every level in the Time Attack phase. You Can Stop Now: Platinum on every level in the Time Attack phase (considered too difficult for one person by Rareware developers)."""
    display_name = "Win Condition"
    option_shuttle_clear = 0
    option_gold_standard = 1
    option_solar_system = 2
    option_gold_time_attack = 3
    option_you_can_stop_now = 4
    default = 0

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["win_condition"] = GoalCondition
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options
