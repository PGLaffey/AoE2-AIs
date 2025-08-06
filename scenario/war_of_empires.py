from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, Comparison, ObjectType, ObjectClass, \
    ObjectState, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player.player import Player
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/war of empires.aoe2scenario'
output_path = f'{scenario_folder}/war of empires - python.aoe2scenario'

xs_path = '../xs/War of Empire.xs'

scenario = AoE2DEScenario.from_file(input_path)
xs_manager = scenario.xs_manager
xs_manager.xs_check.raise_on_error = True
xs_manager.xs_check.ignores.add('DiscardedFn')
xs_manager.xs_check.ignores.add('NoNumPromo')
xs_manager.initialise_xs_trigger(insert_index=0)
xs_manager.add_script(xs_path, validate=True)
t_man = scenario.trigger_manager

# Add Dice Variable Names
for i in range(10):
    try:
        t_man.add_variable(f'Dice {i + 1}', i)
    except ValueError:
        pass


player_list = [
    {'player': 1, 'eco': 3, 'army': 5},
    {'player': 2, 'eco': 6, 'army': 8}
]
# 4 + 7 = Immobile AI
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
                  OtherInfo.FRUIT_BUSH, OtherInfo.TREE_BAMBOO_FOREST, OtherInfo.TREE_PINE_FOREST,
                  (1984, 'Tree (Lush Bamboo Forest)'), (1051, 'Tree (Dragon)'), (1052, 'Tree (Baobab)')]
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
                                         object_list_unit_id=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID)
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
                                         object_list_unit_id=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID)
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
    # Inner + Outer Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        out_gate_x = center.x + (5 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_NORTHWEST_TO_SOUTHEAST.ID)
        trigger.new_effect.create_object(source_player=owner, location_x=out_gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        out_gate_y = center.y + (5 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_SOUTHWEST_TO_NORTHEAST.ID)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=out_gate_y,
                                         object_list_unit_id=BuildingInfo.GATE_SOUTHWEST_TO_NORTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID)
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
    # Inner + Outer Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        out_gate_x = center.x + (5 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_NORTHWEST_TO_SOUTHEAST.ID)
        trigger.new_effect.create_object(source_player=owner, location_x=out_gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        out_gate_y = center.y + (5 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_SOUTHWEST_TO_NORTHEAST.ID)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=out_gate_y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_SOUTHWEST_TO_NORTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.CITY_WALL.ID)
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
    # Inner + Outer Gates
    for x_offset in range(-1, 2, 2):
        gate_x = center.x + (3 * x_offset)
        out_gate_x = center.x + (5 * x_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_NORTHWEST_TO_SOUTHEAST.ID)
        trigger.new_effect.create_object(source_player=owner, location_x=out_gate_x, location_y=center.y + 1,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_NORTHWEST_TO_SOUTHEAST.ID)
    for y_offset in range(-1, 2, 2):
        gate_y = center.y + (3 * y_offset)
        out_gate_y = center.y + (5 * y_offset)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=gate_y,
                                         object_list_unit_id=BuildingInfo.CITY_GATE_SOUTHWEST_TO_NORTHEAST.ID)
        trigger.new_effect.create_object(source_player=owner, location_x=center.x + 1, location_y=out_gate_y,
                                         object_list_unit_id=BuildingInfo.FORTIFIED_GATE_SOUTHWEST_TO_NORTHEAST.ID)
    # Inner Walls
    for tile in wall_area.use_only_edge().to_coords():
        trigger.new_effect.create_object(source_player=owner, location_x=tile.x, location_y=tile.y,
                                         object_list_unit_id=BuildingInfo.CITY_WALL.ID)
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

# --- Heroes ---
HeroInfo.WILLIAM_WALLACE.description = 'Infantry Hero'
HeroInfo.ROBIN_HOOD.description = 'Archer Hero'
HeroInfo.ROBIN_HOOD.modify_stats = {ObjectAttribute.MAX_RANGE: 10}
HeroInfo.ULRICH_VON_JUNGINGEN.description = 'Cavalry Hero'
HeroInfo.GENGHIS_KHAN.description = 'Cavalry Archer Hero'
HeroInfo.ABRAHA_ELEPHANT.description = 'Elephant Hero'
HeroInfo.DAGNAJAN.description = 'Elephant Archer Hero'
HeroInfo.JADWIGA.description = 'Monk Hero'
HeroInfo.JEAN_DE_LORRAIN.description = 'Siege Hero'
heroes = [
    HeroInfo.WILLIAM_WALLACE, # Infantry
    HeroInfo.ROBIN_HOOD, # Archer
    HeroInfo.ULRICH_VON_JUNGINGEN,  # Cav
    HeroInfo.GENGHIS_KHAN,  # Cav Archer
    HeroInfo.ABRAHA_ELEPHANT, # Elephant
    HeroInfo.DAGNAJAN, # Elephant Archer
    HeroInfo.JADWIGA, # Monk
    HeroInfo.JEAN_DE_LORRAIN, # Bombard Cannon
]
hero_tokens_res = Attribute.UNUSED_RESOURCE_010
home_coords_list = [{'area_x1': 0, 'area_y1': 0, 'area_x2': 15, 'area_y2': 15},
               {'area_x1': 265, 'area_y1': 265, 'area_x2': 280, 'area_y2': 280}]
player_colours = ['BLUE', 'RED']
i = 0
for player_group in player_list:
    player = player_group['player']
    player_colour = player_colours[i]
    home_coords = home_coords_list[i]

    # --- Setup Heroes
    hero_setup_trigger = t_man.add_trigger(f'Setup Heroes (p{player})', enabled=True, looping=False)
    j = 1
    for hero in heroes:
        if j == 5:
            j += 1
        hero_setup_trigger.new_effect.change_train_location(source_player=player, object_list_unit_id=hero.ID,
                                                             object_list_unit_id_2=BuildingInfo.TOWER_OF_LONDON.ID,
                                                             button_location=j)
        hero_setup_trigger.new_effect.change_object_cost(source_player=player, object_list_unit_id=hero.ID,
                                                         resource_1=hero_tokens_res, resource_1_quantity=1)
        hero_setup_trigger.new_effect.enable_disable_object(source_player=player, object_list_unit_id=hero.ID,
                                                             enabled=True)
        hero_setup_trigger.new_effect.change_object_description(source_player=player, object_list_unit_id=hero.ID,
                                                                message=f'{hero.description} (Cost: 1 Hero Token)')
        try:
            for stat, value in hero.modify_stats.items():
                hero_setup_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=hero.ID,
                                                               object_attributes=stat,
                                                               operation=Operation.SET, quantity=value)
        except AttributeError:
            pass
        j += 1


    # --- Hero Recruit Token Loop ---
    hero_token_trigger = t_man.add_trigger(f'Add Hero Token (p{player})', enabled=True, looping=False)

    hero_token_loop_trigger = t_man.add_trigger(f'Add Hero Token Loop (p{player})', enabled=False, looping=False)
    hero_token_loop_trigger.new_condition.timer(60)
    hero_token_loop_trigger.new_effect.display_instructions(source_player=player, object_list_unit_id=UnitInfo.KING.ID,
                                                            message=f'<{player_colour}>A New Hero is Available',
                                                            sound_name='hwild1', play_sound=True)
    hero_token_loop_trigger.new_effect.activate_trigger(hero_token_trigger.trigger_id)

    hero_token_trigger.new_effect.modify_resource(source_player=player, tribute_list=hero_tokens_res,
                                                  operation=Operation.ADD, quantity=1)
    hero_token_trigger.new_effect.activate_trigger(hero_token_loop_trigger.trigger_id)

    # --- Display Hero Tokens ---
    hero_token_count_trigger = t_man.add_trigger(f'Display Hero Tokens (p{player})',
                                                 description=f'P{player} Hero Tokens: <{hero_tokens_res.editor_name}, {player}>',
                                                 short_description=f'P{player} Hero Tokens: <{hero_tokens_res.editor_name}, {player}>',
                                                 display_on_screen=True, header=True, description_order=103 - player)
    hero_token_count_trigger.new_condition.player_defeated(PlayerId.GAIA)

    i += 1

defense_function = [rebuild_defense_1, rebuild_defense_2, rebuild_defense_3, rebuild_defense_4, rebuild_defense_5,
                    rebuild_defense_6, rebuild_defense_7, rebuild_defense_8, rebuild_defense_9, rebuild_defense_10]
max_town_level = 10
town_radius = 5
town_locations = [
    # Front Row
    Point(35, 105), # 1
    Point(105, 35), # 2
    # Left Row
    Point(25, 165), # 3
    Point(95, 95),  # 4
    Point(165, 25), # 5
    # Middle Row
    Point(15, 225), # 6
    Point(85, 155), # 7
    Point(155, 85), # 8
    Point(225, 15), # 9
    # Right Row
    Point(75, 215), # 10
    Point(145, 145),# 11
    Point(215, 75), # 12
    # Back Row
    Point(135, 205),# 13
    Point(205, 135) # 14
]
def town_var_id(town_number: int, var: int):
    return (town_number * 10) + var
for town_num in range(1, len(town_locations) + 1):
    # Setup Town Variables
    town_i = town_num - 1
    t_town_var_ids = {
        'owner': 0,
        'eco level': 1,
        'defense level': 2,
        'resource': 3,
        'new owner': 4,
        'center x': 5,
        'center y': 6,
        'rebuild': 7
    }
    town_var_ids = {}
    for var_name, var_i in t_town_var_ids.items():
        try:
            town_var_ids[var_name] = t_man.add_variable(f'Town {town_num} {var_name.capitalize()}', town_var_id(town_num, var_i))
        except ValueError:
            town_var_ids[var_name] = t_man.get_variable(variable_id=town_var_id(town_num, var_i))
    town_center = town_locations[town_i]
    town_area = {'area_x1': town_center.x - town_radius, 'area_x2': town_center.x + town_radius,
                 'area_y1': town_center.y - town_radius, 'area_y2': town_center.y + town_radius}

    # Loop Over Potential Owners
    start_conquer_trigger = t_man.add_trigger(f'Town {town_num} Start Conquer', enabled=True, looping=True)
    conquerer_triggers = []

    for owner in player_list + [player_horde]:
        enemy_players = [player for player in player_list + [player_horde] if player['player'] != owner['player']]


        conquerer_trigger = t_man.add_trigger(f'Town {town_num} Get Conquerer (p{owner["player"]}',
                                              enabled=False, looping=True)
        # Set player as new owner of town if they have troops in town but enemy does not
        conquerer_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area,
                                                        object_type=ObjectType.MILITARY, quantity=1)
        conquerer_trigger.new_condition.or_()
        conquerer_trigger.new_condition.objects_in_area(source_player=owner['army'], **town_area,
                                                         object_type=ObjectType.MILITARY, quantity=1)
        for p in enemy_players:
            conquerer_trigger.new_condition.objects_in_area(source_player=p['player'], **town_area, inverted=True,
                                                            object_type=ObjectType.MILITARY, quantity=1)
            conquerer_trigger.new_condition.objects_in_area(source_player=p['army'], **town_area, inverted=True,
                                                            object_type=ObjectType.MILITARY, quantity=1)
        conquerer_trigger.new_effect.change_variable(variable=town_var_ids['new owner'].variable_id, operation=Operation.SET,
                                                     quantity=owner['player'])
        conquerer_triggers.append(conquerer_trigger)


        # Make town capturable if all towers and fortress are destroyed and it is not marked for rebuilding
        start_conquer_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area, inverted=True,
                                                        object_group=ObjectClass.TOWER, quantity=1)
        start_conquer_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area, inverted=True,
                                                        object_list=BuildingInfo.FORTRESS.ID, quantity=1)
        start_conquer_trigger.new_condition.variable_value(variable=town_var_ids['rebuild'].variable_id, comparison=Comparison.EQUAL,
                                                           quantity=0)
        start_conquer_trigger.new_effect.activate_trigger(conquerer_trigger.trigger_id)
        start_conquer_trigger.new_effect.send_chat(source_player=owner['player'], message=f'Town {town_num} is available for capture. The last team with units within the town will capture it.')


        destroy_trigger = t_man.add_trigger(f'Town {town_num} Destroy (p{owner["player"]})', enabled=True, looping=True)
        destroy_trigger.new_condition.variable_value(variable=town_var_ids['owner'].variable_id, comparison=Comparison.EQUAL,
                                                     quantity=owner['player'])
        destroy_trigger.new_condition.variable_value(variable=town_var_ids['rebuild'].variable_id,
                                                     comparison=Comparison.EQUAL,
                                                     quantity=1)
        # Check there are any units in town area (condition is not more than 1)
        for p in enemy_players + [owner]:
            destroy_trigger.new_condition.objects_in_area(source_player=p['player'], **town_area,
                                                          object_type=ObjectType.MILITARY, quantity=1, inverted=True,
                                                          object_state=ObjectState.ALIVE)
            destroy_trigger.new_condition.objects_in_area(source_player=p['army'], **town_area,
                                                          object_type=ObjectType.MILITARY, quantity=1, inverted=True,
                                                          object_state=ObjectState.ALIVE)
            destroy_trigger.new_effect.kill_object(source_player=p['player'], **town_area,
                                                   object_type=ObjectType.BUILDING)
        destroy_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'].variable_id, operation=Operation.SET,
                                                   quantity=2)
        destroy_trigger.new_effect.send_chat(source_player=1, message=f'Destroying Town {town_num}')
        destroy_area = scenario.new.area()
        destroy_area.center(town_center.x, town_center.y).expand(town_radius)
        for tile in destroy_area.to_coords():
            destroy_trigger.new_effect.create_object(source_player=PlayerId.GAIA, location_x=tile.x, location_y=tile.y,
                                                     object_list_unit_id=UnitInfo.HAWK.ID)
        destroy_trigger.new_effect.kill_object(source_player=PlayerId.GAIA, **town_area,
                                               object_list_unit_id=UnitInfo.HAWK.ID)
        destroy_trigger.new_effect.play_sound(source_player=owner['player'], location_x=town_center.x,
                                              location_y=town_center.y, sound_name='explosion3')

        # Setup Town Rebuild Trigger Per Defense Level
        for defense_level in range(1, len(defense_function) + 1):
            rebuild_trigger = t_man.add_trigger(f'Town {town_num} Rebuild Level {defense_level} (p{owner["player"]})',
                                                enabled=True, looping=True)
            rebuild_trigger.new_condition.variable_value(variable=town_var_ids['owner'].variable_id, comparison=Comparison.EQUAL,
                                                         quantity=owner['player'])
            rebuild_trigger.new_condition.variable_value(variable=town_var_ids['defense level'].variable_id, comparison=Comparison.EQUAL,
                                                         quantity=defense_level)
            rebuild_trigger.new_condition.variable_value(variable=town_var_ids['rebuild'].variable_id, comparison=Comparison.EQUAL,
                                                         quantity=2)
            rebuild_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area, object_type=ObjectType.BUILDING,
                                                          quantity=1, inverted=True, object_state=ObjectState.ALIVE)
            rebuild_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'].variable_id, operation=Operation.SET,
                                                       quantity=0)
            rebuild_trigger.new_effect.send_chat(source_player=owner['player'], message=f'Rebuilding Town {town_num}')
            # Place Building as per Defense Level
            rebuild_trigger.new_effect.send_chat(source_player=1, message=f'Trigger {str(defense_function[defense_level - 1].__name__)} for P{owner["player"]}')
            defense_function[defense_level - 1](rebuild_trigger, owner['player'], town_center, town_area)
            rebuild_area = scenario.new.area()
            rebuild_area.center(town_center.x, town_center.y).expand(town_radius)
            for tile in rebuild_area.to_coords():
                rebuild_trigger.new_effect.create_object(source_player=PlayerId.GAIA, location_x=tile.x,
                                                         location_y=tile.y,
                                                         object_list_unit_id=UnitInfo.HAWK.ID)
            rebuild_trigger.new_effect.kill_object(source_player=PlayerId.GAIA, **town_area,
                                                   object_list_unit_id=UnitInfo.HAWK.ID)
            rebuild_trigger.new_effect.play_sound(source_player=owner['player'], location_x=town_center.x,
                                                  location_y=town_center.y, sound_name='explosion3')
            rebuild_trigger.new_effect.change_object_name(source_player=owner['player'], **town_area,
                                                          object_list_unit_id=OtherInfo.THE_ACCURSED_TOWER.ID,
                                                          message=f'Town {town_num} - Defense {defense_level}')

        # --- Trigger Defense Upgrade ---
        set_upgrade_trigger = t_man.add_trigger(f'Town {town_num} Upgrade Defense (p{owner["player"]})',
                                                enabled=True, looping=True)
        set_upgrade_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area, quantity=1,
                                                          object_list=BuildingInfo.YURT_A.ID, object_state=ObjectState.ALIVE)
        set_upgrade_trigger.new_effect.kill_object(source_player=owner['player'], **town_area,
                                                   object_list_unit_id=BuildingInfo.YURT_A.ID)
        set_upgrade_trigger.new_effect.change_variable(variable=town_var_ids['defense level'].variable_id, operation=Operation.ADD,
                                                       quantity=1)
        set_upgrade_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'].variable_id, operation=Operation.SET,
                                                       quantity=1)
        # --- Defense Max Level ---
        max_defense_trigger = t_man.add_trigger(f'Town {town_num} Max Defense (p{owner["player"]})')
        max_defense_trigger.new_condition.variable_value(variable=town_var_ids['defense level'].variable_id,
                                                         comparison=Comparison.LARGER, quantity=max_town_level)
        max_defense_trigger.new_condition.variable_value(variable=town_var_ids['owner'].variable_id,
                                                         comparison=Comparison.EQUAL, quantity=owner["player"])
        max_defense_trigger.new_effect.change_variable(variable=town_var_ids['defense level'].variable_id,
                                                       operation=Operation.SUBTRACT, quantity=1)
        max_defense_trigger.new_effect.send_chat(source_player=owner['player'], message=f'Town {town_num} defense already at max level')

        # --- Trigger Defense Rebuild ---
        set_rebuild_trigger = t_man.add_trigger(f'Town {town_num} Rebuild Defense (p{owner["player"]})',
                                                enabled=True, looping=True)
        set_rebuild_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area, quantity=1,
                                                          object_list=BuildingInfo.YURT_B.ID, object_state=ObjectState.ALIVE)
        set_rebuild_trigger.new_effect.kill_object(source_player=owner['player'], **town_area,
                                                   object_list_unit_id=BuildingInfo.YURT_B.ID)
        set_rebuild_trigger.new_effect.change_variable(variable=town_var_ids['rebuild'].variable_id, operation=Operation.SET,
                                                       quantity=1)

        # --- Trigger Eco Upgrade ---
        set_eco_upgrade_trigger = t_man.add_trigger(f'Town {town_num} Upgrade Eco (p{owner["player"]})',
                                                    enabled=True, looping=True)
        set_eco_upgrade_trigger.new_condition.objects_in_area(source_player=owner['player'], **town_area, quantity=1,
                                                          object_list=BuildingInfo.YURT_C.ID, object_state=ObjectState.ALIVE)
        set_eco_upgrade_trigger.new_effect.kill_object(source_player=owner['player'], **town_area,
                                                   object_list_unit_id=BuildingInfo.YURT_C.ID)
        set_eco_upgrade_trigger.new_effect.script_call(message=f'town_{town_num}_up_eco();')
        # --- Max Eco Level ---
        max_eco_trigger = t_man.add_trigger(f'Town {town_num} Max Eco (p{owner["player"]})')
        max_eco_trigger.new_condition.variable_value(variable=town_var_ids['eco level'].variable_id,
                                                         comparison=Comparison.LARGER, quantity=max_town_level)
        max_eco_trigger.new_condition.variable_value(variable=town_var_ids['owner'].variable_id,
                                                         comparison=Comparison.EQUAL, quantity=owner["player"])
        max_eco_trigger.new_effect.change_variable(variable=town_var_ids['eco level'].variable_id,
                                                       operation=Operation.SUBTRACT, quantity=1)
        max_eco_trigger.new_effect.send_chat(source_player=owner['player'], message=f'Town {town_num} eco already at max level')


    # Town Capture
    capture_trigger = t_man.add_trigger(f'Town {town_num} Captured', enabled=True, looping=True)
    capture_trigger.new_condition.variable_value(variable=town_var_ids['new owner'].variable_id, comparison=Comparison.EQUAL,
                                                 quantity=0, inverted=True)
    for p in player_list + [player_horde]:
        capture_trigger.new_condition.objects_in_area(source_player=p['player'], **town_area, quantity=1, inverted=True,
                                                      object_type=ObjectType.MILITARY, object_state=ObjectState.ALIVE)
    for trigger in conquerer_triggers:
        capture_trigger.new_effect.deactivate_trigger(trigger.trigger_id)
    capture_trigger.new_effect.script_call(message=f'town_{town_num}_change_ownership();')
    capture_trigger.new_effect.send_chat(source_player=1, message=f'Town {town_num} Captured')

    # Task Town Workers
    task_town_trigger = t_man.add_trigger(f'Town {town_num} Task Villagers', enabled=True, looping=False)
    task_town_trigger.new_effect.task_object(source_player=7, action_type=ActionType.WORK,
                                             area_x1=town_area['area_x1'] - 10, area_y1=town_area['area_y1'] - 10,
                                             area_x2=town_area['area_x2'] + 10, area_y2=town_area['area_y2'] + 10)

# Init Towns
init_town_trigger = t_man.add_trigger(f'Initialize Towns', enabled=True, looping=False)
init_town_trigger.new_effect.script_call(message='init_towns();')


for player_group in player_list:
    player = player_group['player']

    # --- Player Tech Setup ---
    player_setup_trigger = t_man.add_trigger(f"Player Setup (p{player})")
    player_setup_trigger.new_effect.research_technology(source_player=player, force_research_technology=True,
                                                        technology=658) # No pop limit
    player_setup_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.CONSCRIPTION.ID,
                                                               quantity=10)

    # --- Setup Tower Purchase Upgrades ---
    tower_upgrades_trigger = t_man.add_trigger(f"Town Tower Setup Upgrades (p{player})")
    # Sea Tower Buildable
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.SEA_TOWER.ID,
                                                       object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
                                                       operation=Operation.SET, quantity=0)
    # Defense Upgrade
    tower_upgrades_trigger.new_effect.change_train_location(source_player=player, button_location=1,
                                                            object_list_unit_id_2=OtherInfo.THE_ACCURSED_TOWER.ID,
                                                            object_list_unit_id=BuildingInfo.YURT_A.ID)
    tower_upgrades_trigger.new_effect.change_object_name(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                         message=f'Defense Upgrade')
    tower_upgrades_trigger.new_effect.change_object_cost(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                         resource_1=Attribute.WOOD_STORAGE, resource_1_quantity=100,
                                                         resource_2=Attribute.STONE_STORAGE, resource_2_quantity=200)
    tower_upgrades_trigger.new_effect.change_object_description(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                                message=f'Upgrade Town Defenses <cost>')
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                       object_attributes=ObjectAttribute.TRAIN_TIME, operation=Operation.SET,
                                                       quantity=0)
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.YURT_A.ID,
                                                       object_attributes=ObjectAttribute.ICON_ID,
                                                       operation=Operation.SET, quantity=UnitInfo.STORMY_DOG.ICON_ID)
    tower_upgrades_trigger.new_effect.enable_disable_object(source_player=player, enabled=1,
                                                            object_list_unit_id=BuildingInfo.YURT_A.ID)
    # Repair Defenses
    tower_upgrades_trigger.new_effect.change_train_location(source_player=player, button_location=2,
                                                            object_list_unit_id_2=OtherInfo.THE_ACCURSED_TOWER.ID,
                                                            object_list_unit_id=BuildingInfo.YURT_B.ID)
    tower_upgrades_trigger.new_effect.change_object_name(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                         message=f'Repair Defenses')
    tower_upgrades_trigger.new_effect.change_object_cost(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                         resource_1=Attribute.WOOD_STORAGE, resource_1_quantity=200)
    tower_upgrades_trigger.new_effect.change_object_description(source_player=player,
                                                                object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                                message=f'Repair Town Defenses <cost>')
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                       object_attributes=ObjectAttribute.TRAIN_TIME, operation=Operation.SET,
                                                       quantity=0)
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.YURT_B.ID,
                                                       object_attributes=ObjectAttribute.ICON_ID,
                                                       operation=Operation.SET, quantity=HeroInfo.EMPEROR_IN_A_BARREL.ICON_ID)
    tower_upgrades_trigger.new_effect.enable_disable_object(source_player=player, enabled=1,
                                                            object_list_unit_id=BuildingInfo.YURT_B.ID)
    # Upgrade Eco
    tower_upgrades_trigger.new_effect.change_train_location(source_player=player, button_location=3,
                                                            object_list_unit_id_2=OtherInfo.THE_ACCURSED_TOWER.ID,
                                                            object_list_unit_id=BuildingInfo.YURT_C.ID)
    tower_upgrades_trigger.new_effect.change_object_name(source_player=player, object_list_unit_id=BuildingInfo.YURT_C.ID,
                                                         message=f'Upgrade Eco')
    tower_upgrades_trigger.new_effect.change_object_cost(source_player=player, object_list_unit_id=BuildingInfo.YURT_C.ID,
                                                         resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=100)
    tower_upgrades_trigger.new_effect.change_object_description(source_player=player,
                                                                object_list_unit_id=BuildingInfo.YURT_C.ID,
                                                                message=f'Upgrade Town Eco <cost>')
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.YURT_C.ID,
                                                       object_attributes=ObjectAttribute.TRAIN_TIME, operation=Operation.SET,
                                                       quantity=0)
    tower_upgrades_trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=BuildingInfo.YURT_C.ID,
                                                       object_attributes=ObjectAttribute.ICON_ID,
                                                       operation=Operation.SET, quantity=UnitInfo.VILLAGER_MALE.ICON_ID)
    tower_upgrades_trigger.new_effect.enable_disable_object(source_player=player, enabled=1,
                                                            object_list_unit_id=BuildingInfo.YURT_C.ID)

    # --- Trade Workshop Eco Upgrades ---
    trade_workshop_trigger = t_man.add_trigger(f'Trade Workshop Setup (p{player})')
    # Mill upgrades
    for tech in TechInfo.eco_techs(buildings=BuildingInfo.MILL.ID):
        trade_workshop_trigger.new_effect.change_technology_location(source_player=player, technology=tech.ID,
                                                                     object_list_unit_id_2=BuildingInfo.TRADE_WORKSHOP.ID,
                                                                     button_location=1)
    # Lumbercamp upgrades
    for tech in TechInfo.eco_techs(buildings=BuildingInfo.LUMBER_CAMP.ID):
        trade_workshop_trigger.new_effect.change_technology_location(source_player=player, technology=tech.ID,
                                                                     object_list_unit_id_2=BuildingInfo.TRADE_WORKSHOP.ID,
                                                                     button_location=2)
    # Gold upgrades
    for tech in [TechInfo.GOLD_MINING, TechInfo.GOLD_SHAFT_MINING]:
        trade_workshop_trigger.new_effect.change_technology_location(source_player=player, technology=tech.ID,
                                                                     object_list_unit_id_2=BuildingInfo.TRADE_WORKSHOP.ID,
                                                                     button_location=3)
    # Stone upgrades
    for tech in [TechInfo.STONE_MINING, TechInfo.STONE_SHAFT_MINING]:
        trade_workshop_trigger.new_effect.change_technology_location(source_player=player, technology=tech.ID,
                                                                     object_list_unit_id_2=BuildingInfo.TRADE_WORKSHOP.ID,
                                                                     button_location=4)


print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)