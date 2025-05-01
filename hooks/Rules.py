from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value
from BaseClasses import MultiWorld, CollectionState

from ..Data import location_table

import re

def carrierLevelsCleared(world: World, multiworld: MultiWorld, state: CollectionState, player: int, tier: str):

    easyCarrierLevels = [
        "Argent Towers",
        "Blackridge Works",
        "Carrick Point",
        "Havoc District",
        "Simian Acres"
    ]

    mediumCarrierLevels = [
        "Beeton Tracks",
        "Cromlech Court",
        "Ebony Coast",
        "Echo Marches",
        "Ironstone Mine",
        "Outland Farm",
        "Shuttle Gully",
        "Tempest City"
    ]

    hardCarrierLevels = [
        "Angel City",
        "Crystal Rift",
        "Diamond Sands",
        "Ember Hamlet",
        "Glory Crossing",
        "Obsidian Mile",
        "Oyster Harbor"
        ]

    allCarrierLevels = easyCarrierLevels + mediumCarrierLevels + hardCarrierLevels

    carrierLocations = set()
    if tier == "easy":
        carrierLocations.update(f"{loc} - Carrier Clear" for loc in easyCarrierLevels)
    elif tier == "medium":
        carrierLocations.update(f"{loc} - Carrier Clear" for loc in mediumCarrierLevels)
    elif tier == "hard":
        carrierLocations.update(f"{loc} - Carrier Clear" for loc in hardCarrierLevels)
    else:
        carrierLocations.update(f"{loc} - Carrier Clear" for loc in allCarrierLevels)

    cleared = set()
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in carrierLocations:
                    cleared.add(location)

    return all(state.can_reach(location) for location in cleared)

def carrierCleared(world: World, multiworld: MultiWorld, state: CollectionState, player: int, level: str):
    checked = set()
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name == f"{level} - Carrier Clear": checked.add(location)
    return all(state.can_reach(location) for location in checked)

def locationChecked(world: World, multiworld: MultiWorld, state: CollectionState, player: int, loc: str):
    checked = set()
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name == loc: checked.add(location)
    return all(state.can_reach(location) for location in checked)

def goldsSatisfied(world: World, multiworld: MultiWorld, state: CollectionState, player: int, tier: str):

        carrierLevels = [
            "Argent Towers", "Blackridge Works", "Carrick Point",
            "Havoc District", "Simian Acres", "Beeton Tracks",
            "Cromlech Court", "Ebony Coast", "Echo Marches",
            "Ironstone Mine", "Outland Farm", "Shuttle Gully",
            "Tempest City", "Angel City", "Crystal Rift",
            "Diamond Sands", "Ember Hamlet", "Glory Crossing",
            "Obsidian Mile", "Oyster Harbor"
            ]

        minigameLevels = [
              "Backlash", "J-Bomb", "Sideswipe", "Skyfall",
              "Thunderfist", "Baboon Catacomb", "Bison Ridge",
              "Cobalt Quarry", "Cooter Creek", "Corvine Bluff",
              "Dagger Pass", "Dark Heartland", "Falchion Field",
              "Geode Square", "Gibbon's Gate", "Glander's Ranch",
              "Jade Plateau", "Kipling Plant", "Lizard Island",
              "Magma Peak", "Marine Quarter", "Mars", "Mercury",
              "Mica Park", "Moon", "Moraine Chase", "Morgan Hall",
              "Neptune", "Orion Plaza", "Saline Watch",
              "Salvage Wharf", "Shuttle Clear", "Silver Junction",
              "Skerries", "Sleek Streets", "Twilight Foundry",
              "Venus"
            ]

        # tier options: goldstandard, solarsystem
        if tier == "gold_standard":
            for planet in ["Mars", "Mercury", "Venus", "Neptune"]:
                minigameLevels.remove(planet)

        # Create a new list, of all the locations that need to be checked
        locNamesToCheck = []
        if tier not in ["time_attack_gold", "you_can_stop_now"]:
            for level in carrierLevels:
                locNamesToCheck.append(f"{level} - Carrier Clear")
                locNamesToCheck.append(f"{level} - Buildings Clear")
                locNamesToCheck.append(f"{level} - RDUs Clear")
                locNamesToCheck.append(f"{level} - Survivors Clear")
            for level in minigameLevels:
                locNamesToCheck.append(f"{level} - Gold")
        else:
            for level in carrierLevels + minigameLevels:
                requiredMedal = ""
                if tier == "time_attack_gold": requiredMedal = "Gold"
                else: requiredMedal = "Platinum"
                locNamesToCheck.append(f"{level} - {requiredMedal}")

        # Finally, retrieve the corresponding Location objects
        locsToCheck = set()
        for region in multiworld.regions:
            if region.player == player:
                for location in list(region.locations):
                    if location.name in locNamesToCheck: locsToCheck.add(location)

        return all(state.can_reach(location) for location in locsToCheck)

def canUseVehicle(world: World, multiworld: MultiWorld, state: CollectionState, player: int, vehicle: str):
    """Check whether a given vehicle is received, and whether the player can access any of the places that unlock it in-game.
    This is only really needed for race vehicles."""

    unlockLocations = []

    if vehicle == "Police Car":
        unlockLocations.extend(
            [
                "Argent Towers - Police Car",
                "Beeton Tracks - Police Car"
            ]
        )
    elif vehicle == "The American Dream":
        unlockLocations.extend(
            [
                "Simian Acres - American Dream",
                "Echo Marches - American Dream"
            ]
        )
    elif vehicle == "Muscle Car":
        unlockLocations.extend(
            [
                "Havoc District - Muscle Car",
                "Echo Marches - Muscle Car"
            ]
        )
    elif vehicle == "A-Team Van":
        unlockLocations.extend(
            [
                "Crystal Rift - A-Team Van"
            ]
        )

    # Finally, retrieve the corresponding Location objects
    locsToCheck = set()
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in unlockLocations: locsToCheck.add(location)

    if state.has(vehicle, player) and any(state.can_reach(location) for location in locsToCheck):
        return True
    else: return False

def anyRaceVehicle(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    return any(canUseVehicle(world, multiworld, state, player, v) for v in ["Police Car", "The American Dream", "Muscle Car", "A-Team Van"])

def rankPoints(world: World, multiworld: MultiWorld, state: CollectionState, player: int, points: str):
    """Check if the required rank can be reached with the current state"""
    statePoints: int = 0

    locsChecked = set()

    # First grab all the locations that can be reached at this state
    for loc in state.locations_checked:
        if loc.player == player:
            locsChecked.add(loc)

    # Now tally up the points the player should have
    # Bronze medals are 1 point, Silver medals are 2 points, Gold medals are 3 points
    # For whatever reason, Platinums are only 1 point
    for cLoc in locsChecked:
        if cLoc.name.endswith("- Gold"):
            statePoints += 3
            continue
        elif cLoc.name.endswith("- Silver"):
            statePoints += 2
            continue
        elif cLoc.name.endswith("- Bronze"):
            statePoints += 1
            continue
        elif cLoc.name.endswith("- Platinum"):
            statePoints += 1
            continue
        elif cLoc.name.endswith("- Carrier Clear"):
            # Carrier Clears are automatic Gold
            statePoints += 3
            continue
        # I don't have a metric for how the second medal works yet,
        # Other than that doing ALL following clears gives Gold, so
        # instead I'm going to assume that clearing each stat
        # ultimately EQUATES to a Gold medal
        elif cLoc.name.endswith("- Buildings Clear"):
            statePoints += 1
            continue
        elif cLoc.name.endswith("- RDUs Clear"):
            statePoints += 1
            continue
        elif cLoc.name.endswith("- Survivors Clear"):
            statePoints += 1
            continue
    return statePoints >= int(points)

