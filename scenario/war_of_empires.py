from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, Comparison, ObjectType, ObjectClass, \
    ObjectState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.techs import TechInfo

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/war of empires.aoe2scenario'
output_path = f'{scenario_folder}/war of empires - python.aoe2scenario'

xs_path = 'C:/Program Files (x86)/Steam/steamapps/common/AoE2DE/resources/_common/xs/War of Empire.xs'

scenario = AoE2DEScenario.from_file(input_path)
t_man = scenario.trigger_manager

# Add Dice Variable Names
for i in range(10):
    t_man.add_variable(f'Dice {i + 1}', i)


player_list = [
    {'player': 1, 'eco': 3, 'army': 5},
    {'player': 2, 'eco': 6, 'army': 8}
]
player_horde = {'player': 4, 'eco': 4, 'army': 4}
player_civilians = {'player': 7, 'eco': 7, 'army': 7}

archery_upgrades = [TechInfo.CROSSBOWMAN, TechInfo.ARBALESTER, TechInfo.ELITE_SKIRMISHER, TechInfo.IMPERIAL_SKIRMISHER,
                    TechInfo.HEAVY_CAVALRY_ARCHER, TechInfo.ELITE_ELEPHANT_ARCHER, TechInfo.ELITE_GENITOUR,
                    TechInfo.THUMB_RING, TechInfo.PARTHIAN_TACTICS]
barrack_upgrades = [TechInfo.MAN_AT_ARMS, TechInfo.LONG_SWORDSMAN, TechInfo.TWO_HANDED_SWORDSMAN, TechInfo.CHAMPION,
                    TechInfo.LEGIONARY, TechInfo.ARSON, TechInfo.GAMBESONS, TechInfo.PIKEMAN, TechInfo.HALBERDIER,
                    TechInfo.EAGLE_WARRIOR, TechInfo.ELITE_EAGLE_WARRIOR, (982, 'Elite Fire Lancer'), # Elite Fire Lancer
                    TechInfo.SQUIRES]
stable_upgrades = [TechInfo.LIGHT_CAVALRY, TechInfo.HUSSAR, TechInfo.WINGED_HUSSAR, TechInfo.BLOODLINES,
                   TechInfo.ELITE_SHRIVAMSHA_RIDER, TechInfo.CAVALIER, TechInfo.PALADIN, TechInfo.SAVAR,
                   TechInfo.ELITE_STEPPE_LANCER, TechInfo.HEAVY_CAMEL_RIDER, TechInfo.IMPERIAL_CAMEL_RIDER,
                   TechInfo.ELITE_BATTLE_ELEPHANT, TechInfo.HUSBANDRY, (1033, 'Heavy Hei Guang Cavalry') # Heavy Hei Guang Cavalry
                   ]
siege_upgrades = [TechInfo.CAPPED_RAM, TechInfo.SIEGE_RAM, TechInfo.SIEGE_ELEPHANT, TechInfo.ONAGER,
                  TechInfo.SIEGE_ONAGER, TechInfo.HEAVY_SCORPION, TechInfo.HOUFNICE, (980, 'Heavy Rocket Cart') # Heavy Rocket Cart
                  ]
other_upgrades = [TechInfo.BALLISTICS, TechInfo.CHEMISTRY, TechInfo.SIEGE_ENGINEERS, TechInfo.SPIES_AND_TREASON,
                  TechInfo.FEUDAL_AGE, TechInfo.CASTLE_AGE, TechInfo.IMPERIAL_AGE, TechInfo.TREADMILL_CRANE]

# Add Eco Upgrades
eco_upgrades = TechInfo.eco_techs() + other_upgrades
for player in player_list:
    for tech_obj in eco_upgrades:
        try:
            tech = tech_obj.value[0]
            tech_name = tech_obj.name.capitalize()
        except AttributeError:
            tech = tech_obj[0]
            tech_name = tech_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Research {tech_name} (p{player["player"]})')
        trigger.new_condition.research_technology(source_player=player['player'], technology=tech)
        trigger.new_effect.research_technology(source_player=player['eco'], technology=tech, force_research_technology=True)

# Add Army Upgrades
army_upgrades = (TechInfo.blacksmith_techs() + archery_upgrades + barrack_upgrades + stable_upgrades + siege_upgrades +
                 other_upgrades)
for player in player_list:
    for tech_obj in army_upgrades:
        try:
            tech = tech_obj.value[0]
            tech_name = tech_obj.name.capitalize()
        except AttributeError:
            tech = tech_obj[0]
            tech_name = tech_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Research {tech_name} (p{player["player"]})')
        trigger.new_condition.research_technology(source_player=player['player'], technology=tech)
        trigger.new_effect.research_technology(source_player=player['army'], technology=tech, force_research_technology=True)

# Setup Unlimited Resources
gaia_resources = [OtherInfo.GOLD_MINE, OtherInfo.STONE_MINE, OtherInfo.FORAGE_BUSH, OtherInfo.TREE_OAK_FOREST,
                  OtherInfo.FRUIT_BUSH, OtherInfo.TREE_BAMBOO_FOREST, OtherInfo.TREE_PINE_FOREST]
player_resources = [BuildingInfo.FARM]
for res_obj in gaia_resources:
    try:
        res = res_obj.ID
        res_name = res_obj.name.capitalize()
    except AttributeError:
        res = res_obj[0]
        res_name = res_obj[1].capitalize()
    trigger = t_man.add_trigger(f'Resource {res_name}')
    trigger.new_effect.modify_attribute(operation=Operation.SET, source_player=PlayerId.GAIA, object_list_unit_id=res,
                                        object_attributes=ObjectAttribute.DEAD_UNIT_ID, quantity=res)
for player in player_list:
    for res_obj in player_resources:
        try:
            res = res_obj.ID
            res_name = res_obj.name.capitalize()
        except AttributeError:
            res = res_obj[0]
            res_name = res_obj[1].capitalize()
        trigger = t_man.add_trigger(f'Resource {res_name} (p{player["player"]})')
        trigger.new_effect.modify_attribute(operation=Operation.SET, source_player=player['eco'], quantity=res,
                                            object_list_unit_id=res, object_attributes=ObjectAttribute.DEAD_UNIT_ID)

# ===== Towns =====
# 1: Tower
def rebuild_defense_1(trigger: Trigger, owner: int, center: Point, town_area: dict):
    trigger.new_effect.kill_object(source_player=owner, **town_area, object_type=ObjectType.BUILDING)
    trigger.new_effect.create_object(source_player=owner, location_x=center.x,
                                     location_y=center.y, object_list_unit_id=OtherInfo.THE_ACCURSED_TOWER.ID)

# 2: 1 + Palisade Wall
def rebuild_defense_2(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center,town_area)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(2)
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x,
                                         location_y=tile.y, object_list_unit_id=BuildingInfo.FORTIFIED_PALISADE_WALL.ID)

# 3: Bigger 2 + Sea Towers on Corners
def rebuild_defense_3(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.SEA_TOWER.ID)
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_PALISADE_WALL.ID)

# 4: 3 + Gates, extra walls and Watch tower (Gates spawn is +ve most point)
def rebuild_defense_4(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.SEA_TOWER.ID)
        tower_wall = scenario.new.area()
        tower_wall.center(tile.x, tile.y).expand(1)
        for tower_tile in tower_wall.to_coords():
            trigger.new_effect.create_object(source_player=owner, location_x=tower_tile.x, location_y=tower_tile.y,
                                             object_list_unit_id=BuildingInfo.FORTIFIED_PALISADE_WALL.ID)
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.PALISADE_GATE_SOUTHWEST_TO_NORTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.PALISADE_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_PALISADE_WALL.ID)

# 5: 4 but stone walls + Guard towers
def rebuild_defense_5(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.GUARD_TOWER.ID)
        tower_wall = scenario.new.area()
        tower_wall.center(tile.x, tile.y).expand(1)
        for tower_tile in list(set(tower_wall.to_coords()) - set(tower_wall.use_only_corners().to_coords())):
            trigger.new_effect.create_object(source_player=owner, location_x=tower_tile.x, location_y=tower_tile.y,
                                             object_list_unit_id=BuildingInfo.STONE_WALL.ID)
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.STONE_WALL.ID)

# 6: 5 + short outer Palisade + Guard towers
def rebuild_defense_6(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_5(trigger, owner, center, town_area)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=3, gap_size=1)
    for tile in wall_area.to_coords():
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2'] \
            or tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.FORTIFIED_PALISADE_WALL.ID)
    tower_area = scenario.new.area()
    tower_area.center(center.x, center.y).expand(4).use_pattern_grid(block_size=1, gap_size=3)
    for tile in tower_area.to_coords():
        if tile.x == town_area['area_x1'] + 1 or tile.x == town_area['area_x2'] - 1 or tile.x == center.x:
            if tile.y == town_area['area_y1'] + 1 or tile.y == town_area['area_y2'] - 1 or tile.y == center.y:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.GUARD_TOWER.ID)

# 7: 6 + east Fortress (Fortress center is -1 -1 from +ve most point)
def rebuild_defense_7(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    trigger.new_effect.create_object(source_player=owner, location_x=center.x -3, location_y=center.y - 3,
                                     object_list_unit_id=BuildingInfo.FORTRESS.ID)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    # Inner Towers
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.GUARD_TOWER.ID)
        tower_wall = scenario.new.area()
        tower_wall.center(tile.x, tile.y).expand(1)
        for tower_tile in list(set(tower_wall.to_coords()) - set(tower_wall.use_only_corners().to_coords())):
            trigger.new_effect.create_object(source_player=owner, location_x=tower_tile.x, location_y=tower_tile.y,
                                             object_list_unit_id=BuildingInfo.STONE_WALL.ID)
    # Inner Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.STONE_WALL.ID)
    # Outer Walls
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=3, gap_size=1)
    for tile in wall_area.to_coords():
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2'] \
            or tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.FORTIFIED_PALISADE_WALL.ID)
    # Outer Towers
    tower_area = scenario.new.area()
    tower_area.center(center.x, center.y).expand(4).use_pattern_grid(block_size=1, gap_size=3)
    for tile in tower_area.to_coords():
        if tile.x == town_area['area_x1'] + 1 or tile.x == town_area['area_x2'] - 1 or tile.x == center.x:
            if tile.y == town_area['area_y1'] + 1 or tile.y == town_area['area_y2'] - 1 or tile.y == center.y:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.GUARD_TOWER.ID)

# 8: 7 + full walls + wall upgrade + Bombard towers
def rebuild_defense_8(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    trigger.new_effect.create_object(source_player=owner, location_x=center.x -3, location_y=center.y - 3,
                                     object_list_unit_id=BuildingInfo.FORTRESS.ID)
    # Bombard Towers
    bomb_area = scenario.new.area()
    bomb_area.center(center.x, center.y).expand(1)
    for tile in bomb_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.BOMBARD_TOWER.ID)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    # Inner Towers
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.GUARD_TOWER.ID)
        tower_wall = scenario.new.area()
        tower_wall.center(tile.x, tile.y).expand(1)
        for tower_tile in list(set(tower_wall.to_coords()) - set(tower_wall.use_only_corners().to_coords())):
            trigger.new_effect.create_object(source_player=owner, location_x=tower_tile.x, location_y=tower_tile.y,
                                             object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID)
    # Inner Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_SOUTHWEST_TO_NORTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID)
    # Outer Gates
    gate_area = scenario.new.area()
    gate_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=1, gap_size=4)
    for tile in list(gate_area.to_coords()):
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2']:
            if tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                continue
            trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                             object_list_unit_id=BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID)
        if tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
            if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2']:
                continue
            trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                             object_list_unit_id=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Outer Walls
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=3, gap_size=1)
    for tile in wall_area.to_coords():
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2'] \
            or tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.STONE_WALL.ID)
    # Outer Towers
    tower_area = scenario.new.area()
    tower_area.center(center.x, center.y).expand(4).use_pattern_grid(block_size=1, gap_size=3)
    for tile in tower_area.to_coords():
        if tile.x == town_area['area_x1'] + 1 or tile.x == town_area['area_x2'] - 1 or tile.x == center.x:
            if tile.y == town_area['area_y1'] + 1 or tile.y == town_area['area_y2'] - 1 or tile.y == center.y:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.GUARD_TOWER.ID)

# 9: 8 + upgraded walls + keep
def rebuild_defense_9(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    trigger.new_effect.create_object(source_player=owner, location_x=center.x -3, location_y=center.y - 3,
                                     object_list_unit_id=BuildingInfo.FORTRESS.ID)
    # Bombard Towers
    bomb_area = scenario.new.area()
    bomb_area.center(center.x, center.y).expand(1)
    for tile in bomb_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.BOMBARD_TOWER.ID)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    # Inner Towers
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.KEEP.ID)
        tower_wall = scenario.new.area()
        tower_wall.center(tile.x, tile.y).expand(1)
        for tower_tile in list(set(tower_wall.to_coords()) - set(tower_wall.use_only_corners().to_coords())):
            trigger.new_effect.create_object(source_player=owner, location_x=tower_tile.x, location_y=tower_tile.y,
                                             object_list_unit_id=BuildingInfo.CITY_WALL.ID)
    # Inner Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_SOUTHWEST_TO_NORTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.CITY_WALL.ID)
    # Outer Gates
    gate_area = scenario.new.area()
    gate_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=1, gap_size=4)
    for tile in list(gate_area.to_coords()):
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2']:
            if tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                continue
            trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                             object_list_unit_id=BuildingInfo.FORTIFIED_GATE_SOUTHWEST_TO_NORTHEAST.ID)
        if tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
            if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2']:
                continue
            trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                             object_list_unit_id=BuildingInfo.FORTIFIED_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Outer Walls
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=3, gap_size=1)
    for tile in wall_area.to_coords():
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2'] \
            or tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID)
    # Outer Towers
    tower_area = scenario.new.area()
    tower_area.center(center.x, center.y).expand(4).use_pattern_grid(block_size=1, gap_size=3)
    for tile in tower_area.to_coords():
        if tile.x == town_area['area_x1'] + 1 or tile.x == town_area['area_x2'] - 1 or tile.x == center.x:
            if tile.y == town_area['area_y1'] + 1 or tile.y == town_area['area_y2'] - 1 or tile.y == center.y:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.KEEP.ID)

# 10: 9 + Fortress west + Fire towers
def rebuild_defense_10(trigger: Trigger, owner: int, center: Point, town_area: dict):
    rebuild_defense_1(trigger, owner, center, town_area)
    trigger.new_effect.create_object(source_player=owner, location_x=center.x -3, location_y=center.y - 3,
                                     object_list_unit_id=BuildingInfo.FORTRESS.ID)
    trigger.new_effect.create_object(source_player=owner, location_x=center.x + 4, location_y=center.y + 4,
                                     object_list_unit_id=BuildingInfo.FORTRESS.ID)
    # Fire Towers
    bomb_area = scenario.new.area()
    bomb_area.center(center.x, center.y).expand(1)
    for tile in bomb_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.FIRE_TOWER.ID)
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(3)
    # Inner Towers
    for tile in wall_area.use_only_corners().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.KEEP.ID)
        tower_wall = scenario.new.area()
        tower_wall.center(tile.x, tile.y).expand(1)
        for tower_tile in list(set(tower_wall.to_coords()) - set(tower_wall.use_only_corners().to_coords())):
            trigger.new_effect.create_object(source_player=owner, location_x=tower_tile.x, location_y=tower_tile.y,
                                             object_list_unit_id=BuildingInfo.CITY_WALL.ID)
    # Inner Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_SOUTHWEST_TO_NORTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.CITY_WALL.ID)
    # Outer Gates
    gate_area = scenario.new.area()
    gate_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=1, gap_size=4)
    for tile in list(gate_area.to_coords()):
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2']:
            if tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                continue
            trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                             object_list_unit_id=BuildingInfo.FORTIFIED_GATE_SOUTHWEST_TO_NORTHEAST.ID)
        if tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
            if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2']:
                continue
            trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                             object_list_unit_id=BuildingInfo.FORTIFIED_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    # Outer Walls
    wall_area = scenario.new.area()
    wall_area.center(center.x, center.y).expand(5).use_pattern_grid(block_size=3, gap_size=1)
    for tile in wall_area.to_coords():
        if tile.x == town_area['area_x1'] or tile.x == town_area['area_x2'] \
            or tile.y == town_area['area_y1'] or tile.y == town_area['area_y2']:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID)
    # Outer Towers
    tower_area = scenario.new.area()
    tower_area.center(center.x, center.y).expand(4).use_pattern_grid(block_size=1, gap_size=3)
    for tile in tower_area.to_coords():
        if tile.x == town_area['area_x1'] + 1 or tile.x == town_area['area_x2'] - 1 or tile.x == center.x:
            if tile.y == town_area['area_y1'] + 1 or tile.y == town_area['area_y2'] - 1 or tile.y == center.y:
                trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                                 object_list_unit_id=BuildingInfo.KEEP.ID)

# TODO Add more heroes
heroes = [HeroInfo.ABRAHA_ELEPHANT, HeroInfo.GENGHIS_KHAN]
# town_count = 10
defense_function = [rebuild_defense_1, rebuild_defense_2, rebuild_defense_3, rebuild_defense_4, rebuild_defense_5,
                    rebuild_defense_6, rebuild_defense_7, rebuild_defense_8, rebuild_defense_9, rebuild_defense_10]
town_radius = 5
town_locations = [
    Point(50, 50) # TODO Add more locations
]
def town_var_id(town_number: int, var: int):
    return (town_number * 10) + var
for town_num in range(1, len(town_locations) + 1):
    # Setup Town Variables
    town_i = town_num - 1
    town_var_ids = {
        'owner': 0,
        'eco level': 1,
        'defense level': 2,
        'resource': 3,
        'new owner': 4,
        'center x': 5,
        'center y': 6,
        'rebuild': 7
    }
    for var_name, var_i in town_var_ids.items():
        town_var_ids[var_name] = t_man.add_variable(var_name.capitalize(), town_var_id(town_num, var_i))
    town_center = town_locations[town_i]
    town_area = {'area_x1': town_center.x - town_radius, 'area_x2': town_center.x + town_radius,
                 'area_y1': town_center.y - town_radius, 'area_y2': town_center.y + town_radius}
    # Loop Over Potential Owners
    for owner in player_list:
        enemy_players = [player for player in player_list if player['player'] != owner['player']] + [player_horde]
        # Setup Town Rebuild Trigger Per Defense Level
        for defense_level in range(1, len(defense_function) + 1):
            rebuild_trigger = t_man.add_trigger(f'Town {town_num} Rebuild Level {defense_level} (p{owner["player"]})',
                                                enabled=True, looping=True)
            rebuild_trigger.new_condition.variable_value(variable=town_var_ids['defense level'], comparison=Comparison.EQUAL,
                                                         quantity=defense_level)
            rebuild_trigger.new_condition.variable_value(variable=town_var_ids['rebuild'], comparison=Comparison.EQUAL,
                                                         quantity=1)
            # Check there are any units in town area (condition is not more than 1)
            for p in enemy_players + [owner]:
                rebuild_trigger.new_condition.objects_in_area(source_player=p['player'], **town_area,
                                                              object_type=ObjectType.MILITARY, quantity=1, inverted=True,
                                                              object_state=ObjectState.ALIVE)
                rebuild_trigger.new_condition.objects_in_area(source_player=p['army'], **town_area,
                                                              object_type=ObjectType.MILITARY, quantity=1, inverted=True,
                                                              object_state=ObjectState.ALIVE)

            rebuild_trigger.new_effect.send_chat(source_player=owner['player'], message=f'Rebuilding Town {town_num}')
            # Place Building as per Defense Level
            defense_function[defense_level - 1](rebuild_trigger, owner['player'], town_center, town_area)
            rebuild_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'], operation=Operation.SET,
                                                       quantity=0)

        # --- Trigger Upgrade ---
        set_upgrade_trigger = t_man.add_trigger(f'Town {town_num} Upgrade Defense (p{owner["player"]})',
                                                enabled=True, looping=True)
        set_upgrade_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area,
                                                          object_list=BuildingInfo.YURT_A.ID, object_state=ObjectState.FOUNDATION)
        set_upgrade_trigger.new_effect.kill_object(source_player=owner['player'], **town_area,
                                                   object_list_unit_id=BuildingInfo.YURT_A.ID)
        set_upgrade_trigger.new_effect.change_variable(variable=town_var_ids['defense level'], operation=Operation.ADD,
                                                       quantity=1)
        set_upgrade_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'], operation=Operation.SET,
                                                       quantity=1)
        # --- Trigger Rebuild ---
        set_rebuild_trigger = t_man.add_trigger(f'Town {town_num} Rebuild Defense (p{owner["player"]})',
                                                enabled=True, looping=True)
        set_rebuild_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area,
                                                          object_list=BuildingInfo.YURT_B.ID, object_state=ObjectState.FOUNDATION)
        set_rebuild_trigger.new_effect.kill_object(source_player=owner['player'], **town_area,
                                                   object_list_unit_id=BuildingInfo.YURT_B.ID)
        set_upgrade_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'], operation=Operation.SET,
                                                       quantity=1)


# Setup Tower Purchase Upgrades
for player_group in player_list:
    player = player_group['player']
    tower_upgrades_trigger = t_man.add_trigger(f"Tower Upgrades Trigger (p{player})")
    # Defense Upgrade
    tower_upgrades_trigger.new_effect.change_train_location(source_player=player, button_location=1,
                                                            object_list_unit_id=OtherInfo.THE_ACCURSED_TOWER.ID,
                                                            object_list_unit_id_2=BuildingInfo.YURT_A.ID)
    tower_upgrades_trigger.new_effect.change_object_name(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                         message=f'Defense Upgrade')
    tower_upgrades_trigger.new_effect.change_object_cost(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                         resource_1=ObjectAttribute.WOOD_COSTS, resource_1_quantity=10)
    tower_upgrades_trigger.new_effect.change_object_icon(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                         object_list_unit_id_2=BuildingInfo.FORTRESS.ICON_ID)
    tower_upgrades_trigger.new_effect.change_object_description(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                                message=f'Upgrade Town Defenses <cost>')
    # Repair Defenses
    tower_upgrades_trigger.new_effect.change_train_location(source_player=player, button_location=2,
                                                            object_list_unit_id=OtherInfo.THE_ACCURSED_TOWER.ID,
                                                            object_list_unit_id_2=BuildingInfo.YURT_B.ID)
    tower_upgrades_trigger.new_effect.change_object_name(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                         message=f'Repair Defenses')
    tower_upgrades_trigger.new_effect.change_object_cost(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                         resource_1=ObjectAttribute.WOOD_COSTS, resource_1_quantity=5)
    tower_upgrades_trigger.new_effect.change_object_icon(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                         object_list_unit_id_2=BuildingInfo.BLACKSMITH.ICON_ID)
    tower_upgrades_trigger.new_effect.change_object_description(source_player=player,
                                                                object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                                message=f'Repair Town Defenses <cost>')

print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)