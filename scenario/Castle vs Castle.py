import shutil

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, Comparison, ObjectType, ObjectClass, \
    ObjectState, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.player.player import Player
from AoE2ScenarioParser.objects.data_objects.player.player_resources import PlayerResources
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute
from util import *
import dotenv
import os

class PlayerNum:
    def __init__(self, num: int, army: int):
        self.num = num
        self.army = army

    def __len__(self):
        return 2

    def __getitem__(self, item):
        return [self.num, self.army][item]

dotenv.load_dotenv()
scenario_folder = f'C:/Users/{os.getenv("username", "User")}/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/Castle vs Castle.aoe2scenario'
output_path = f'{scenario_folder}/Castle vs Castle - python.aoe2scenario'

xs_path = '../xs/Castle vs Castle.xs'

scenario = AoE2DEScenario.from_file(input_path)
xs_manager = scenario.xs_manager
xs_manager.xs_check.raise_on_error = True
xs_manager.xs_check.ignores.add('DiscardedFn')
xs_manager.xs_check.ignores.add('NoNumPromo')
xs_manager.initialise_xs_trigger(insert_index=0)
# xs_manager.add_script(xs_path, validate=True)
t_man = scenario.trigger_manager
unit_man = scenario.unit_manager


map_x, map_y = scenario.map_manager.map_width, scenario.map_manager.map_height

ai_goals = {
    'toggle_swordsman': {1: 10, 2: 20, 3: 30, 6: 40},
    'toggle_spearman': {1: 11, 2: 21, 3: 31, 6: 41},
    'toggle_alt_infantry': {1: 12, 2: 22, 3: 32, 6: 42},
    'toggle_archer': {1: 13, 2: 23, 3: 33, 6: 43},
    'toggle_skirmisher': {1: 14, 2: 24, 3: 34, 6: 44},
    'toggle_cav_archer': {1: 15, 2: 25, 3: 35, 6: 45},
    'toggle_light_cav': {1: 16, 2: 26, 3: 36, 6: 46},
    'toggle_heavy_cav': {1: 17, 2: 27, 3: 37, 6: 47},
    'toggle_alt_cav': {1: 18, 2: 28, 3: 38, 6: 48},
    'toggle_unique_unit': {1: 19, 2: 29, 3: 39, 6: 49}
}

players = [PlayerNum(1, 5), PlayerNum(2, 8), PlayerNum(3, 4), PlayerNum(6, 7)]
res_villagers = Attribute.UNUSED_RESOURCE_008

silver_crown_icon = TechInfo.INQUISITION.ICON_ID
gold_crown_icon = TechInfo.SUPREMACY.ICON_ID

for player, army in players:
    setup_res = t_man.add_trigger(f'Setup Resources (p{player})', enabled=True, looping=False)

    setup_res.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.SET, quantity=50)
    setup_res.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.SUBTRACT, quantity=3)

    setup_army = t_man.add_trigger(f'Setup Army (p{player})', enabled=True, looping=False)
    setup_army.new_effect.research_technology(source_player=army, force_research_technology=True,
                                              technology=TechInfo.SET_MAXIMUM_POPULATION_NO_HOUSES.ID)

    next_age = None
    for i, age in enumerate(reversed([TechInfo.FEUDAL_AGE, TechInfo.CASTLE_AGE, TechInfo.IMPERIAL_AGE])):
        army_age = t_man.add_trigger(f'Age {age.name} (p{player})', enabled=i==2, looping=False)
        army_age.new_condition.research_technology(source_player=player, technology=age.ID)
        army_age.new_effect.research_technology(source_player=army, technology=age.ID, force_research_technology=True)
        if next_age is not None:
            army_age.new_effect.activate_trigger(next_age.trigger_id)
        next_age = army_age

    # Villager Limit
    vil_limit = t_man.add_trigger(f'Villager Limit (p{player})', enabled=True, looping=False)
    for unit in UnitInfo.vils():
        vil_limit.new_effect.change_object_cost(source_player=player, object_list_unit_id=unit.ID,
                                                resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=50,
                                                resource_2=res_villagers, resource_2_quantity=1)
        vil_limit.new_effect.modify_attribute(source_player=player, object_list_unit_id=unit.ID,
                                              object_attributes=ObjectAttribute.DEAD_UNIT_ID, operation=Operation.SET,
                                              quantity=OtherInfo.IMPALED_CORPSE.ID)
    # Villager Dies
    vil_died = t_man.add_trigger(f'Villager Died (p{player})', enabled=True, looping=True)
    vil_died.new_condition.own_objects(source_player=player, object_list=OtherInfo.IMPALED_CORPSE.ID, quantity=1)
    vil_died.new_effect.remove_object(source_player=player, object_list_unit_id=OtherInfo.IMPALED_CORPSE.ID, max_units_affected=1)
    vil_died.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.ADD, quantity=1)

    # -------------------------
    # ----- Army Barracks -----
    # -------------------------
    tech_infantry_time = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_0.ID, name='Infantry Training Time', icon=TechInfo.SQUIRES.ICON_ID,
        description='Trains Infantry 10% Faster', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_swordsman = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_1.ID, name='Upgrade Swordsman Line', icon=TechInfo.CHAMPION.ICON_ID,
        description='Improves the Swordsman line', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_spearman = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_2.ID, name='Upgrade Spearman Line', icon=TechInfo.HALBERDIER.ICON_ID,
        description='Improves the Spearman line', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_alt_infantry = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_3.ID, name='Upgrade Alternative Infantry Line',
        icon=TechInfo.ELITE_EAGLE_WARRIOR.ICON_ID, description='Improves the Alternative Infantry line',
        cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_toggle_swordsman = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_4.ID, name='Enable creating Swordsman Line', icon=silver_crown_icon,
        description='Continuously creates Swordsman line to add to the army', cost=[], research_time=5)
    tech_toggle_spearman = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_5.ID, name='Enable creating Spearman Line', icon=silver_crown_icon,
        description='Continuously creates Spearman line to add to the army', cost=[], research_time=5)
    tech_toggle_alt_infantry = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_6.ID, name='Enable creating Alternative Infantry Line', icon=silver_crown_icon,
        description='Continuously creates Alternative Infantry line to add to the army', cost=[], research_time=5)
    barracks_techs = [(tech_toggle_swordsman, 1), (tech_toggle_spearman, 2), (tech_toggle_alt_infantry, 3),
                      (tech_upgrade_swordsman, 6), (tech_upgrade_spearman, 7), (tech_upgrade_alt_infantry, 8),
                      (tech_infantry_time, 15)]
    camp_barracks = t_man.add_trigger(f'Camp Barracks (p{player})', enabled=True, looping=False)
    building = BuildingInfo.CAMP_BARRACKS.ID
    for tech, location in barracks_techs:
        tech.add_to_building(player, building, location, camp_barracks)

    swordsman_units = [UnitInfo.MILITIA, UnitInfo.MAN_AT_ARMS, UnitInfo.LONG_SWORDSMAN, UnitInfo.TWO_HANDED_SWORDSMAN,
                       UnitInfo.CHAMPION, UnitInfo.LEGIONARY], 60
    spearman_units = [UnitInfo.SPEARMAN, UnitInfo.PIKEMAN, UnitInfo.HALBERDIER, UnitInfo.HEAVY_PIKEMAN], 60 #TODO UnitInfo.SPARABARA
    alt_infantry_1_units = [UnitInfo.EAGLE_SCOUT, UnitInfo.EAGLE_WARRIOR, UnitInfo.ELITE_EAGLE_WARRIOR], 80
    alt_infantry_2_units = [UnitInfo.FIRE_LANCER, UnitInfo.ELITE_FIRE_LANCER], 80
    alt_infantry_units = (alt_infantry_1_units[0] + alt_infantry_2_units[0],)
    barracks_units = swordsman_units[0] + spearman_units[0] + alt_infantry_1_units[0] + alt_infantry_2_units[0]

    infantry_training_setup = t_man.add_trigger(f'Init Infantry Training Time (p{player})', enabled=True, looping=False)
    for units, train_time in [swordsman_units, spearman_units, alt_infantry_1_units, alt_infantry_2_units]:
        for unit in units:
            infantry_training_setup.new_effect.modify_attribute(
                source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
                operation=Operation.SET, quantity=train_time
            )
            infantry_training_setup.new_effect.change_object_cost(source_player=army, object_list_unit_id=unit.ID)

    infantry_training_time = t_man.add_trigger(f'Research Infantry Training Time (p{player})', enabled=True, looping=True)
    infantry_training_time.new_condition.research_technology(source_player=player, technology=tech_infantry_time.ID)
    tech_infantry_time.update(trigger=infantry_training_time, player=player, cost=1.15)
    for unit in barracks_units:
        infantry_training_time.new_effect.modify_attribute(
            source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
            operation=Operation.MULTIPLY, quantity=0.9
        )

    # Infantry Upgrades
    swordman_upgrades = [
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1)],
        [TechInfo.MAN_AT_ARMS, (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.BUILDING), 3)],
        [TechInfo.LONG_SWORDSMAN, (ObjectAttribute.MOVEMENT_SPEED, 1.1)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 1), (ObjectAttribute.HIT_POINTS, 10)],
        [TechInfo.TWO_HANDED_SWORDSMAN, (ObjectAttribute.MOVEMENT_SPEED, 1.1)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 2), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.75)],
        [TechInfo.CHAMPION, (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.BUILDING), 5)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.INFANTRY), 4), (ObjectAttribute.BLAST_ATTACK_LEVEL, 2),
         (ObjectAttribute.AREA_DAMAGE, -5), (ObjectAttribute.BLAST_WIDTH, 0.5)],
        [TechInfo.LEGIONARY, (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 3)]
    ]
    spearman_upgrades = [
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 1), (ObjectAttribute.MOVEMENT_SPEED, 1.1)],
        [TechInfo.PIKEMAN, (ObjectAttribute.MAXIMUM_RANGE, 0.5)],
        [(ObjectAttribute.HIT_POINTS, 10), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.75)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [TechInfo.HALBERDIER],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(ObjectAttribute.MOVEMENT_SPEED, 1.1), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 1)],
        [(UnitInfo.HEAVY_PIKEMAN, UnitInfo.HALBERDIER, BuildingInfo.BARRACKS, 2),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.CAVALRY), 28), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.CAMEL), 12),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.ELEPHANT), 10), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 3),
         (ObjectAttribute.ATTACK_RELOAD_TIME, 0.75)],
        [(ObjectAttribute.MAXIMUM_RANGE, 1), (ObjectAttribute.HIT_POINTS, 10)]
    ]
    alt_infantry_upgrades = [
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.CAVALRY), 3)],
        [(ObjectAttribute.MOVEMENT_SPEED, 1.1), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.ARCHER), 3),
         (ObjectAttribute.HIT_POINTS, 10)],
        [TechInfo.EAGLE_WARRIOR, (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.BUILDING), 5)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.75)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.ARCHER), 3), (ObjectAttribute.HIT_POINTS, 10),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.CAVALRY), 3)],
        [(ObjectAttribute.MOVEMENT_SPEED, 1.1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1)],
        [TechInfo.ELITE_EAGLE_WARRIOR, TechInfo.ELITE_FIRE_LANCER, (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(ObjectAttribute.ATTACK_RELOAD_TIME, 0.75), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.BUILDING), 5)],
        [(ObjectAttribute.MOVEMENT_SPEED, 1.1), (ObjectAttribute.HIT_POINTS, 10)]
    ]
    infantry_upgrades = [('Swordsman', tech_upgrade_swordsman, swordman_upgrades, swordsman_units),
                         ('Spearman', tech_upgrade_spearman, spearman_upgrades, spearman_units),
                         ('Alt Infantry', tech_upgrade_alt_infantry, alt_infantry_upgrades, alt_infantry_units)]

    # Toggle Swordsman
    enable_toggle_swordsman = t_man.add_trigger(f'Research Enable Toggle Swordsman (p{player})', enabled=True, looping=False)
    disable_toggle_swordsman = t_man.add_trigger(f'Research Disable Toggle Swordsman (p{player})', enabled=False, looping=False)
    enable_toggle_swordsman.new_condition.research_technology(source_player=player, technology=tech_toggle_swordsman.ID)
    enable_toggle_swordsman.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_swordsman'][player])
    tech_toggle_swordsman.update(player=player, trigger=enable_toggle_swordsman, name='Disable creating Swordsman Line',
                                 icon=gold_crown_icon, description='Stop creating Swordsman line for the army')
    enable_toggle_swordsman.new_effect.activate_trigger(disable_toggle_swordsman.trigger_id)
    disable_toggle_swordsman.new_condition.research_technology(source_player=player, technology=tech_toggle_swordsman.ID)
    disable_toggle_swordsman.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_swordsman'][player])
    tech_toggle_swordsman.update(player=player, trigger=disable_toggle_swordsman, name='Enable creating Swordsman Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Swordsman line to add to the army')
    disable_toggle_swordsman.new_effect.activate_trigger(enable_toggle_swordsman.trigger_id)
    # Toggle Spearman
    enable_toggle_spearman = t_man.add_trigger(f'Research Enable Toggle Spearman (p{player})', enabled=True, looping=False)
    disable_toggle_spearman = t_man.add_trigger(f'Research Disable Toggle Spearman (p{player})', enabled=False, looping=False)
    enable_toggle_spearman.new_condition.research_technology(source_player=player, technology=tech_toggle_spearman.ID)
    enable_toggle_spearman.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_spearman'][player])
    tech_toggle_spearman.update(player=player, trigger=enable_toggle_spearman, name='Disable creating Spearman Line',
                                 icon=gold_crown_icon, description='Stop creating Spearman line for the army')
    enable_toggle_spearman.new_effect.activate_trigger(disable_toggle_spearman.trigger_id)
    disable_toggle_spearman.new_condition.research_technology(source_player=player, technology=tech_toggle_spearman.ID)
    disable_toggle_spearman.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_spearman'][player])
    tech_toggle_spearman.update(player=player, trigger=disable_toggle_spearman, name='Enable creating Spearman Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Spearman line to add to the army')
    disable_toggle_spearman.new_effect.activate_trigger(enable_toggle_spearman.trigger_id)

    # Toggle Alt Infantry
    enable_toggle_alt_infantry = t_man.add_trigger(f'Research Enable Toggle Alt Infantry (p{player})', enabled=True, looping=False)
    disable_toggle_alt_infantry = t_man.add_trigger(f'Research Disable Toggle Alt Infantry (p{player})', enabled=False, looping=False)
    enable_toggle_alt_infantry.new_condition.research_technology(source_player=player, technology=tech_toggle_alt_infantry.ID)
    enable_toggle_alt_infantry.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_alt_infantry'][player])
    tech_toggle_alt_infantry.update(player=player, trigger=enable_toggle_alt_infantry, name='Disable creating Alternative Infantry Line',
                                 icon=gold_crown_icon, description='Stop creating Alternative Infantry line for the army')
    enable_toggle_alt_infantry.new_effect.activate_trigger(disable_toggle_alt_infantry.trigger_id)
    disable_toggle_alt_infantry.new_condition.research_technology(source_player=player, technology=tech_toggle_alt_infantry.ID)
    disable_toggle_alt_infantry.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_alt_infantry'][player])
    tech_toggle_alt_infantry.update(player=player, trigger=disable_toggle_alt_infantry, name='Enable creating Alternative Infantry Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Alternative Infantry line to add to the army')
    disable_toggle_alt_infantry.new_effect.activate_trigger(enable_toggle_alt_infantry.trigger_id)

    # Camp Archery Range
    tech_archer_time = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_7.ID, name='Archer Training Time', icon=TechInfo.PARTHIAN_TACTICS.ICON_ID,
        description='Trains Archers 10% Faster', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_archer = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_8.ID, name='Upgrade Archer Line', icon=TechInfo.ARBALESTER.ICON_ID,
        description='Improves the Archer line', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_skirmisher = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_9.ID, name='Upgrade Skirmisher Line', icon=TechInfo.IMPERIAL_SKIRMISHER.ICON_ID,
        description='Improves the Skirmisher line', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_cav_archer = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_10.ID, name='Upgrade Mounted Archer Line',
        icon=TechInfo.HEAVY_CAVALRY_ARCHER.ICON_ID, description='Improves the Mounted Archer line',
        cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_toggle_archer = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_11.ID, name='Enable creating Archer Line', icon=silver_crown_icon,
        description='Continuously creates Archer line to add to the army', cost=[], research_time=5)
    tech_toggle_skirmisher = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_12.ID, name='Enable creating Skirmisher Line', icon=silver_crown_icon,
        description='Continuously creates Skirmisher line to add to the army', cost=[], research_time=5)
    tech_toggle_cav_archer = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_13.ID, name='Enable creating Mounted Archer Line', icon=silver_crown_icon,
        description='Continuously creates Mounted Archer line to add to the army', cost=[], research_time=5)
    archery_techs = [(tech_toggle_archer, 1), (tech_toggle_skirmisher, 2), (tech_toggle_cav_archer, 3),
                      (tech_upgrade_archer, 6), (tech_upgrade_skirmisher, 7), (tech_upgrade_cav_archer, 8),
                      (tech_archer_time, 15)]
    camp_archery = t_man.add_trigger(f'Camp Archery Range (p{player})', enabled=True, looping=False)
    for tech, location in archery_techs:
        tech.add_to_building(player, BuildingInfo.CAMP_ARCHERY_RANGE.ID, location, camp_archery)

    archer_units = [UnitInfo.ARCHER, UnitInfo.CROSSBOWMAN, UnitInfo.ARBALESTER, UnitInfo.HEAVY_CROSSBOWMAN], 70
    skirmisher_units = [UnitInfo.SKIRMISHER, UnitInfo.ELITE_SKIRMISHER, UnitInfo.IMPERIAL_SKIRMISHER, UnitInfo.MERCENARY_PELTAST], 60
    cav_archer_1_units = [UnitInfo.CAVALRY_ARCHER, UnitInfo.HEAVY_CAVALRY_ARCHER,UnitInfo.SCYTHIAN_HORSE_ARCHER, UnitInfo.KHAN], 80
    cav_archer_2_units = [UnitInfo.ELEPHANT_ARCHER, UnitInfo.ELITE_ELEPHANT_ARCHER], 90
    cav_archer_units = (cav_archer_1_units[0] + cav_archer_2_units[0],)
    archery_range_units = archer_units[0] + skirmisher_units[0] + cav_archer_1_units[0] + cav_archer_2_units[0]

    archer_training_setup = t_man.add_trigger(f'Init Archer Training Time (p{player})', enabled=True, looping=False)
    for units, train_time in [archer_units, skirmisher_units, cav_archer_1_units, cav_archer_2_units]:
        for unit in units:
            archer_training_setup.new_effect.modify_attribute(
                source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
                operation=Operation.SET, quantity=train_time
            )
            archer_training_setup.new_effect.change_object_cost(source_player=army, object_list_unit_id=unit.ID)

    archer_training_time = t_man.add_trigger(f'Research Archer Training Time (p{player})', enabled=True, looping=True)
    archer_training_time.new_condition.research_technology(source_player=player, technology=tech_archer_time.ID)
    tech_archer_time.update(trigger=archer_training_time, player=player, cost=1.15)
    for unit in archery_range_units:
        archer_training_time.new_effect.modify_attribute(
            source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
            operation=Operation.MULTIPLY, quantity=0.9
        )

    archer_upgrades = [
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.PIERCE), 1), (ObjectAttribute.MAXIMUM_RANGE, 1)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [TechInfo.CROSSBOWMAN, (ObjectAttribute.ATTACK_RELOAD_TIME, 0.85)],
        [(ObjectAttribute.HIT_POINTS, 10), (ObjectAttribute.LINE_OF_SIGHT, 2), (ObjectAttribute.MAXIMUM_RANGE, 1)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.INFANTRY), 4)],
        [TechInfo.ARBALESTER, (ObjectAttribute.MAXIMUM_RANGE, 1), (ObjectAttribute.LINE_OF_SIGHT, 2),
         (ObjectAttribute.MAXIMUM_TOTAL_MISSILES, 1), (ObjectAttribute.TOTAL_MISSILES, 1)],
        [(ObjectAttribute.HIT_POINTS, 10), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.PIERCE), 1),
         (ObjectAttribute.ATTACK_RELOAD_TIME, 0.85)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1),
         (ObjectAttribute.MAXIMUM_RANGE, 1)],
        [(UnitInfo.HEAVY_CROSSBOWMAN, UnitInfo.ARBALESTER, BuildingInfo.ARCHERY_RANGE, 1),
         (ObjectAttribute.ATTACK_RELOAD_TIME, 0.4)],
        [(ObjectAttribute.MAXIMUM_TOTAL_MISSILES, 2), (ObjectAttribute.TOTAL_MISSILES, 2), (ObjectAttribute.MAXIMUM_RANGE, 1)],
    ]
    skirmisher_upgrades = [
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.85),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.PIERCE), 1)],
        [(ObjectAttribute.MAXIMUM_RANGE, 1), (ObjectAttribute.HIT_POINTS, 10),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.ARCHER), 2), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.CAVALRY_ARCHER), 1)],
        [TechInfo.ELITE_SKIRMISHER, (ObjectAttribute.ATTACK_RELOAD_TIME, 0.85), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.PIERCE), 1), (ObjectAttribute.MAXIMUM_RANGE, 1)],
        [(ObjectAttribute.HIT_POINTS, 10), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.85)],
        [TechInfo.IMPERIAL_SKIRMISHER, (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.ARCHER), 2)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.PIERCE), 1), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.85)],
        [(ObjectAttribute.HIT_POINTS, 10), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1)],
        [(UnitInfo.MERCENARY_PELTAST, UnitInfo.IMPERIAL_SKIRMISHER, BuildingInfo.ARCHERY_RANGE, 2),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.ARCHER), 5), (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.CAVALRY_ARCHER), 6),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.INFANTRY), 5), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 4)],
        [(ObjectAttribute.MAXIMUM_RANGE, 1), (ObjectAttribute.MAXIMUM_TOTAL_MISSILES, 9), (ObjectAttribute.TOTAL_MISSILES, 9),
         (ObjectAttribute.HIT_POINTS, 10)],
    ]
    cav_archer_upgrades = [
        [(ObjectAttribute.HIT_POINTS, 10), (ObjectAttribute.MOVEMENT_SPEED, 1.1)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [TechInfo.HEAVY_CAVALRY_ARCHER, (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.INFANTRY), 3), (ObjectAttribute.MAXIMUM_RANGE, 1)],
        [(ObjectAttribute.ATTACK_RELOAD_TIME, 0.80), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1),
         (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(ObjectAttribute.HIT_POINTS, 10), (ObjectAttribute.MOVEMENT_SPEED, 1.1), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1)],
        [(UnitInfo.SCYTHIAN_HORSE_ARCHER, UnitInfo.HEAVY_CAVALRY_ARCHER, BuildingInfo.ARCHERY_RANGE, 3),
         TechInfo.ELITE_ELEPHANT_ARCHER, (ObjectAttribute.ATTACK_RELOAD_TIME, 0.80), (ObjectAttribute.HIT_POINTS, 20),
         (AttackArmor(ObjectAttribute.ATTACK, A_TYPE.PIERCE), 2), (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1)],
        [(AttackArmor(ObjectAttribute.ATTACK, A_TYPE.INFANTRY), 4), (ObjectAttribute.MOVEMENT_SPEED, 1.1),
         (AttackArmor(ObjectAttribute.ARMOR, A_TYPE.PIERCE), 1), (ObjectAttribute.ATTACK_RELOAD_TIME, 0.80)],
        [(AttackArmor(ObjectAttribute.ARMOR, A_TYPE.MELEE), 1), (ObjectAttribute.HIT_POINTS, 20)],
        [(UnitInfo.KHAN, UnitInfo.SCYTHIAN_HORSE_ARCHER, BuildingInfo.ARCHERY_RANGE, 3), (ObjectAttribute.MOVEMENT_SPEED, 1.1)],
        [(ObjectAttribute.ATTACK_RELOAD_TIME, 0.80)]
    ]
    archery_unit_upgrade = [('Archer', tech_upgrade_archer, archer_upgrades, archer_units),
                            ('Skirmisher', tech_upgrade_skirmisher, skirmisher_upgrades, skirmisher_units),
                            ('Cav Archer', tech_upgrade_cav_archer, cav_archer_upgrades, cav_archer_units)]

    # Toggle Archer
    enable_toggle_archer = t_man.add_trigger(f'Research Enable Toggle Archer (p{player})', enabled=True, looping=False)
    disable_toggle_archer = t_man.add_trigger(f'Research Disable Toggle Archer (p{player})', enabled=False, looping=False)
    enable_toggle_archer.new_condition.research_technology(source_player=player, technology=tech_toggle_archer.ID)
    enable_toggle_archer.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_archer'][player])
    tech_toggle_archer.update(player=player, trigger=enable_toggle_archer, name='Disable creating Archer Line',
                                 icon=gold_crown_icon, description='Stop creating Archer line for the army')
    enable_toggle_archer.new_effect.activate_trigger(disable_toggle_archer.trigger_id)
    disable_toggle_archer.new_condition.research_technology(source_player=player, technology=tech_toggle_archer.ID)
    disable_toggle_archer.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_archer'][player])
    tech_toggle_archer.update(player=player, trigger=disable_toggle_archer, name='Enable creating Archer Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Archer line to add to the army')
    disable_toggle_archer.new_effect.activate_trigger(enable_toggle_archer.trigger_id)
    # Toggle Skirmisher
    enable_toggle_skirmisher = t_man.add_trigger(f'Research Enable Toggle Skirmisher (p{player})', enabled=True, looping=False)
    disable_toggle_skirmisher = t_man.add_trigger(f'Research Disable Toggle Skirmisher (p{player})', enabled=False, looping=False)
    enable_toggle_skirmisher.new_condition.research_technology(source_player=player, technology=tech_toggle_skirmisher.ID)
    enable_toggle_skirmisher.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_skirmisher'][player])
    tech_toggle_skirmisher.update(player=player, trigger=enable_toggle_skirmisher, name='Disable creating Skirmisher Line',
                                icon=gold_crown_icon, description='Stop creating Skirmisher line for the army')
    enable_toggle_skirmisher.new_effect.activate_trigger(disable_toggle_skirmisher.trigger_id)
    disable_toggle_skirmisher.new_condition.research_technology(source_player=player, technology=tech_toggle_skirmisher.ID)
    disable_toggle_skirmisher.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_skirmisher'][player])
    tech_toggle_skirmisher.update(player=player, trigger=disable_toggle_skirmisher, name='Enable creating Skirmisher Line',
                                icon=silver_crown_icon,
                                description='Continuously creates Skirmisher line to add to the army')
    disable_toggle_skirmisher.new_effect.activate_trigger(enable_toggle_skirmisher.trigger_id)

    # Toggle Cav Archer
    enable_toggle_cav_archer = t_man.add_trigger(f'Research Enable Toggle Cav Archer (p{player})', enabled=True, looping=False)
    disable_toggle_cav_archer = t_man.add_trigger(f'Research Disable Toggle Cav Archer (p{player})', enabled=False, looping=False)
    enable_toggle_cav_archer.new_condition.research_technology(source_player=player, technology=tech_toggle_cav_archer.ID)
    enable_toggle_cav_archer.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_cav_archer'][player])
    tech_toggle_cav_archer.update(player=player, trigger=enable_toggle_cav_archer, name='Disable creating Mounted Archer Line',
                                 icon=gold_crown_icon, description='Stop creating Mounted Archer line for the army')
    enable_toggle_cav_archer.new_effect.activate_trigger(disable_toggle_cav_archer.trigger_id)
    disable_toggle_cav_archer.new_condition.research_technology(source_player=player, technology=tech_toggle_cav_archer.ID)
    disable_toggle_cav_archer.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_cav_archer'][player])
    tech_toggle_cav_archer.update(player=player, trigger=disable_toggle_cav_archer, name='Enable creating Mounted Archer Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Mounted Archer line to add to the army')
    disable_toggle_cav_archer.new_effect.activate_trigger(enable_toggle_cav_archer.trigger_id)

    # -----------------------
    # ----- Army Stable -----
    # -----------------------
    tech_cavalry_time = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_14.ID, name='Cavalry Training Time', icon=TechInfo.HUSBANDRY.ICON_ID,
        description='Trains Cavalry 10% Faster', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_light_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_15.ID, name='Upgrade Light Cavalry Line', icon=TechInfo.WINGED_HUSSAR.ICON_ID,
        description='Improves the Light Cavalry line', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_heavy_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_16.ID, name='Upgrade Heavy Cavalry Line', icon=TechInfo.PALADIN.ICON_ID,
        description='Improves the Heavy Cavalry line', cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_alt_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_17.ID, name='Upgrade Alternative Cavalry Line',
        icon=TechInfo.HEAVY_CAVALRY_ARCHER.ICON_ID, description='Improves the Alternative Cavalry line',
        cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_toggle_light_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_18.ID, name='Enable creating Light Cavalry Line', icon=silver_crown_icon,
        description='Continuously creates Light Cavalry line to add to the army', cost=[], research_time=5)
    tech_toggle_heavy_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_19.ID, name='Enable creating Heavy Cavalry Line',
        icon=silver_crown_icon, description='Continuously creates Heavy Cavalry line to add to the army',
        cost=[], research_time=5)
    tech_toggle_alt_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_20.ID, name='Enable creating Alternative Cavalry Line',
        icon=silver_crown_icon, description='Continuously creates Alternative Cavalry line to add to the army',
        cost=[], research_time=5)
    stable_techs = [(tech_toggle_light_cav, 1), (tech_toggle_heavy_cav, 2), (tech_toggle_alt_cav, 3),
                     (tech_upgrade_light_cav, 6), (tech_upgrade_heavy_cav, 7), (tech_upgrade_alt_cav, 8),
                     (tech_cavalry_time, 15)]
    camp_stable = t_man.add_trigger(f'Camp Stable (p{player})', enabled=True, looping=False)
    for tech, location in stable_techs:
        tech.add_to_building(player, BuildingInfo.CAMP_STABLE.ID, location, camp_stable)

    light_cav_units = [UnitInfo.SCOUT_CAVALRY, UnitInfo.LIGHT_CAVALRY, UnitInfo.HUSSAR, UnitInfo.WINGED_HUSSAR], 60
    heavy_cav_1_units = [UnitInfo.KNIGHT, UnitInfo.CAVALIER, UnitInfo.PALADIN, UnitInfo.CRUSADER_KNIGHT], 70
    heavy_cav_2_units = [UnitInfo.STEPPE_LANCER, UnitInfo.ELITE_STEPPE_LANCER, UnitInfo.SOGDIAN_CATAPHRACT], 60
    heavy_cav_3_units = [UnitInfo.SHRIVAMSHA_RIDER, UnitInfo.ELITE_SHRIVAMSHA_RIDER, UnitInfo.GREEK_NOBLE_CAVALRY], 60
    heavy_cav_4_units = [UnitInfo.HEI_GUANG_CAVALRY, UnitInfo.HEAVY_HEI_GUANG_CAVALRY, UnitInfo.CRUSADER_KNIGHT], 70
    heavy_cav_units = (heavy_cav_1_units[0] + heavy_cav_2_units[0] + heavy_cav_3_units[0] + heavy_cav_4_units[0],)
    alt_cav_1_units = [UnitInfo.CAMEL_SCOUT, UnitInfo.CAMEL_RIDER, UnitInfo.HEAVY_CAMEL_RIDER, UnitInfo.IMPERIAL_CAMEL_RIDER], 60
    alt_cav_2_units = [UnitInfo.BATTLE_ELEPHANT, UnitInfo.ELITE_BATTLE_ELEPHANT, UnitInfo.SANNAHYA], 80
    alt_cav_units = (alt_cav_1_units[0] + alt_cav_2_units[0],)
    stable_units = light_cav_units[0] + heavy_cav_units[0] + alt_cav_units[0]

    cavalry_training_setup = t_man.add_trigger(f'Init Cavalry Training Time (p{player})', enabled=True, looping=False)
    for units, train_time in [light_cav_units, heavy_cav_1_units, heavy_cav_2_units, heavy_cav_3_units, heavy_cav_4_units, alt_cav_1_units, alt_cav_2_units]:
        for unit in units:
            cavalry_training_setup.new_effect.modify_attribute(
                source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
                operation=Operation.SET, quantity=train_time
            )
            cavalry_training_setup.new_effect.change_object_cost(source_player=army, object_list_unit_id=unit.ID)

    cavalry_training_time = t_man.add_trigger(f'Research Cavalry Training Time (p{player})', enabled=True, looping=True)
    cavalry_training_time.new_condition.research_technology(source_player=player, technology=tech_cavalry_time.ID)
    tech_cavalry_time.update(trigger=cavalry_training_time, player=player, cost=1.15)
    for unit in stable_units:
        cavalry_training_time.new_effect.modify_attribute(
            source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
            operation=Operation.MULTIPLY, quantity=0.9
        )

    light_cav_upgrades = [
        [],
        [],
        [TechInfo.LIGHT_CAVALRY],
        [],
        [],
        [TechInfo.HUSSAR],
        [],
        [],
        [TechInfo.WINGED_HUSSAR],
        []
    ]
    heavy_cav_upgrades = [
        [],
        [],
        [TechInfo.CAVALIER],
        [TechInfo.ELITE_STEPPE_LANCER, TechInfo.ELITE_SHRIVAMSHA_RIDER],
        [],
        [TechInfo.PALADIN],
        [],
        [(UnitInfo.SOGDIAN_CATAPHRACT, UnitInfo.ELITE_STEPPE_LANCER, BuildingInfo.STABLE, 4),
         (UnitInfo.GREEK_NOBLE_CAVALRY, UnitInfo.ELITE_SHRIVAMSHA_RIDER, BuildingInfo.STABLE, 2)],
        [(UnitInfo.CRUSADER_KNIGHT, UnitInfo.PALADIN, BuildingInfo.STABLE, 2),
         (UnitInfo.CRUSADER_KNIGHT, UnitInfo.HEAVY_HEI_GUANG_CAVALRY, BuildingInfo.STABLE, 2)],
        []
    ]
    alt_cav_upgrades = [
        [],
        [TechInfo.UPGRADE_CAMEL_SCOUTS_TO_RIDERS],
        [],
        [TechInfo.ELITE_BATTLE_ELEPHANT],
        [TechInfo.HEAVY_CAMEL_RIDER],
        [],
        [],
        [TechInfo.IMPERIAL_CAMEL_RIDER, (UnitInfo.SANNAHYA, UnitInfo.ELITE_BATTLE_ELEPHANT, BuildingInfo.STABLE, 4)],
        [],
        []
    ]
    cavalry_unit_upgrades = [('Light Cavalry', tech_upgrade_light_cav, light_cav_upgrades, light_cav_units),
                             ('Heavy Cavalry', tech_upgrade_heavy_cav, heavy_cav_upgrades, heavy_cav_units),
                             ('Alt Cavalry', tech_upgrade_alt_cav, alt_cav_upgrades, alt_cav_units)]

    # Toggle Light Cavalry
    enable_toggle_light_cav = t_man.add_trigger(f'Research Enable Toggle Light Cavalry (p{player})', enabled=True, looping=False)
    disable_toggle_light_cav = t_man.add_trigger(f'Research Disable Toggle Light Cavalry (p{player})', enabled=False, looping=False)
    enable_toggle_light_cav.new_condition.research_technology(source_player=player, technology=tech_toggle_light_cav.ID)
    enable_toggle_light_cav.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_light_cav'][player])
    tech_toggle_light_cav.update(player=player, trigger=enable_toggle_light_cav, name='Disable creating Light Cavalry Line',
                                 icon=gold_crown_icon, description='Stop creating Light Cavalry line for the army')
    enable_toggle_light_cav.new_effect.activate_trigger(disable_toggle_light_cav.trigger_id)
    disable_toggle_light_cav.new_condition.research_technology(source_player=player, technology=tech_toggle_light_cav.ID)
    disable_toggle_light_cav.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_light_cav'][player])
    tech_toggle_light_cav.update(player=player, trigger=disable_toggle_light_cav, name='Enable creating Light Cavalry Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Light Cavalry line to add to the army')
    disable_toggle_light_cav.new_effect.activate_trigger(enable_toggle_light_cav.trigger_id)
    # Toggle Heavy Cavalry
    enable_toggle_heavy_cav = t_man.add_trigger(f'Research Enable Toggle Heavy Cavalry (p{player})', enabled=True, looping=False)
    disable_toggle_heavy_cav = t_man.add_trigger(f'Research Disable Toggle Heavy Cavalry (p{player})', enabled=False, looping=False)
    enable_toggle_heavy_cav.new_condition.research_technology(source_player=player, technology=tech_toggle_heavy_cav.ID)
    enable_toggle_heavy_cav.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_heavy_cav'][player])
    tech_toggle_heavy_cav.update(player=player, trigger=enable_toggle_heavy_cav, name='Disable creating Heavy Cavalry Line',
                                 icon=gold_crown_icon, description='Stop creating Heavy Cavalry line for the army')
    enable_toggle_heavy_cav.new_effect.activate_trigger(disable_toggle_heavy_cav.trigger_id)
    disable_toggle_heavy_cav.new_condition.research_technology(source_player=player, technology=tech_toggle_heavy_cav.ID)
    disable_toggle_heavy_cav.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_heavy_cav'][player])
    tech_toggle_heavy_cav.update(player=player, trigger=disable_toggle_heavy_cav, name='Enable creating Heavy Cavalry Line',
                                 icon=silver_crown_icon,
                                 description='Continuously creates Heavy Cavalry line to add to the army')
    disable_toggle_heavy_cav.new_effect.activate_trigger(enable_toggle_heavy_cav.trigger_id)
    # Toggle Alt Cavalry
    enable_toggle_alt_cav = t_man.add_trigger(f'Research Enable Toggle Alt Cavalry (p{player})', enabled=True, looping=False)
    disable_toggle_alt_cav = t_man.add_trigger(f'Research Disable Toggle Alt Cavalry (p{player})', enabled=False, looping=False)
    enable_toggle_alt_cav.new_condition.research_technology(source_player=player, technology=tech_toggle_alt_cav.ID)
    enable_toggle_alt_cav.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_alt_cav'][player])
    tech_toggle_alt_cav.update(player=player, trigger=enable_toggle_alt_cav, name='Disable creating Alt Cavalry Line',
                               icon=gold_crown_icon, description='Stop creating Alt Cavalry line for the army')
    enable_toggle_alt_cav.new_effect.activate_trigger(disable_toggle_alt_cav.trigger_id)
    disable_toggle_alt_cav.new_condition.research_technology(source_player=player, technology=tech_toggle_alt_cav.ID)
    disable_toggle_alt_cav.new_effect.ai_script_goal(ai_script_goal=ai_goals['toggle_alt_cav'][player])
    tech_toggle_alt_cav.update(player=player, trigger=disable_toggle_alt_cav, name='Enable creating Alt Cavalry Line',
                               icon=silver_crown_icon,
                               description='Continuously creates Alt Cavalry line to add to the army')
    disable_toggle_alt_cav.new_effect.activate_trigger(enable_toggle_alt_cav.trigger_id)

    all_unit_upgrades = infantry_upgrades + archery_unit_upgrade + cavalry_unit_upgrades
    for name, upgrade_tech, unit_upgrades, units in infantry_upgrades:
        next_upgrade = None
        for i, upgrades in enumerate(reversed(unit_upgrades)):
            level = 10 - i
            up_trigger = t_man.add_trigger(f'Upgrade {name} Level {level} (p{player})', enabled=level == 1, looping=False)
            up_trigger.new_condition.research_technology(source_player=player, technology=upgrade_tech.ID)
            for upgrade in upgrades:
                if type(upgrade) == TechInfo:
                    up_trigger.new_effect.research_technology(source_player=army, technology=upgrade.ID,
                                                              force_research_technology=True)
                elif type(upgrade[0]) == UnitInfo:
                    new_unit, old_unit, building, location = upgrade
                    replace_unit(trigger=up_trigger, player=army, new_unit=new_unit, old_unit=old_unit, building=building,
                                 location=location)
                else:
                    upgrade, quantity = upgrade
                    adjust_unit(trigger=up_trigger, player=army, units=units[0], attribute=upgrade, quantity=quantity)
            if next_upgrade is not None:
                cost = 50 + (50 * level)
                if level > 3:
                    cost += 50 * (level - 3)
                if level > 6:
                    cost += 50 * (level - 6)
                if level > 8:
                    cost += 50 * (level - 8)
                upgrade_tech.update(player=player, trigger=up_trigger, cost=cost)
                up_trigger.new_effect.activate_trigger(next_upgrade.trigger_id)
            next_upgrade = up_trigger

print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)
    ai_path = f'{os.getenv("steam_path", "C:/Program Files (x86)/Steam")}/steamapps/common/AoE2DE/resources/_common/ai'
    shutil.copy('../ai/Castle vs Castle.per', f'{ai_path}/Castle vs Castle.per')
    shutil.copytree('../ai/castle_vs_castle', f'{ai_path}/castle_vs_castle', dirs_exist_ok=True)
