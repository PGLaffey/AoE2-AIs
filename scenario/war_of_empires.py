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
def rebuild_defense_1(trigger: Trigger, vars: dict):
    trigger.new_effect.create_object(source_player=vars['owner'], location_x=vars['center x'],
                                     location_y=vars['center y'], object_list_unit_id=OtherInfo.THE_ACCURSED_TOWER)

# TODO Add more heroes
heroes = [HeroInfo.ABRAHA_ELEPHANT, HeroInfo.GENGHIS_KHAN]
town_count = 10
town_max_defense_level = 10
town_radius = 5
town_locations = [
    Point(10, 10) # TODO Add more locations
]
def town_var_id(town_number: int, var: int):
    return (town_number * 10) + var
for town_num in range(1, town_count + 1):
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
        for defense_level in range(1, town_max_defense_level + 1):
            rebuild_trigger = t_man.add_trigger(f'Town {town_num} Rebuild Level {defense_level} (p{owner["player"]})')
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
            if defense_level == 1:
                rebuild_defense_1(rebuild_trigger, town_vars)



print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)