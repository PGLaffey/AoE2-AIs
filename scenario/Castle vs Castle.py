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

class PlayerNum:
    def __init__(self, num: int, army: int):
        self.num = num
        self.army = army

    def __len__(self):
        return 2

    def __getitem__(self, item):
        return [self.num, self.army][item]


scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
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
    'toggle_alt_infantry': {1: 12, 2: 22, 3: 32, 6: 42}
}

players = [PlayerNum(1, 5), PlayerNum(2, 8), PlayerNum(3, 4), PlayerNum(6, 7)]
res_villagers = Attribute.UNUSED_RESOURCE_008

silver_crown_icon = TechInfo.INQUISITION.ICON_ID
gold_crown_icon = TechInfo.SUPREMACY.ICON_ID

for player, army in players:
    setup_res = t_man.add_trigger(f'Setup Resources (p{player})', enabled=True, looping=False)

    setup_res.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.SET, quantity=50)
    setup_res.new_effect.modify_resource(source_player=player, tribute_list=res_villagers, operation=Operation.SUBTRACT, quantity=3)

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
                       UnitInfo.CHAMPION], 60
    spearman_units = [UnitInfo.SPEARMAN, UnitInfo.PIKEMAN, UnitInfo.HALBERDIER], 60
    alt_infantry_1_units = [UnitInfo.EAGLE_SCOUT, UnitInfo.EAGLE_WARRIOR, UnitInfo.ELITE_EAGLE_WARRIOR], 80
    alt_infantry_2_units = [UnitInfo.FIRE_LANCER, UnitInfo.ELITE_FIRE_LANCER], 80
    barracks_units = swordsman_units[0] + spearman_units[0] + alt_infantry_1_units[0] + alt_infantry_2_units[0]

    infantry_training_setup = t_man.add_trigger(f'Init Infantry Training Time (p{player})', enabled=True, looping=False)
    for units, train_time in [swordsman_units, spearman_units, alt_infantry_1_units, alt_infantry_2_units]:
        for unit in units:
            infantry_training_setup.new_effect.modify_object_attribute(
                source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
                operation=Operation.SET, quantity=train_time
            )

    infantry_training_time = t_man.add_trigger(f'Research Infantry Training Time (p{player})', enabled=True, looping=True)
    infantry_training_time.new_condition.research_technology(source_player=player, technology=tech_infantry_time.ID)
    infantry_training_time.new_effect.enable_disable_technology(source_player=player, technology=tech_infantry_time.ID, enabled=True)
    for unit in barracks_units:
        infantry_training_time.new_effect.modify_attribute(
            source_player=army, object_list_unit_id=unit.ID, object_attributes=ObjectAttribute.TRAIN_TIME,
            operation=Operation.MULTIPLY, quantity=0.9
        )

    ## TODO upgrades


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
    building = BuildingInfo.CAMP_ARCHERY_RANGE.ID
    for tech, location in archery_techs:
        tech.add_to_building(player, building, location, camp_archery)

    # -----------------------
    # ----- Army Stable -----
    # -----------------------
    tech_cavalry_time = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_14.ID, name='Cavalry Training Time',
        icon=TechInfo.HUSBANDRY.ICON_ID,
        description='Trains Cavalry 10% Faster',
        cost=[(Attribute.FOOD_STORAGE, 250), (Attribute.GOLD_STORAGE, 200)])
    tech_upgrade_light_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_15.ID, name='Upgrade Light Cavalry Line', icon=TechInfo.WINGED_HUSSAR_POLES.ICON_ID,
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
        icon=silver_crown_icon,
        description='Continuously creates Heavy Cavalry line to add to the army', cost=[], research_time=5)
    tech_toggle_alt_cav = CustomTech(
        override_tech=TechInfo.BLANK_TECHNOLOGY_20.ID, name='Enable creating Alternative Cavalry Line',
        icon=silver_crown_icon,
        description='Continuously creates Alternative Cavalry line to add to the army', cost=[], research_time=5)
    stable_techs = [(tech_toggle_archer, 1), (tech_toggle_skirmisher, 2), (tech_toggle_cav_archer, 3),
                     (tech_upgrade_archer, 6), (tech_upgrade_skirmisher, 7), (tech_upgrade_cav_archer, 8),
                     (tech_archer_time, 15)]
    camp_stable = t_man.add_trigger(f'Camp Stable (p{player})', enabled=True, looping=False)
    building = BuildingInfo.CAMP_STABLE.ID
    for tech, location in stable_techs:
        tech.add_to_building(player, building, location, camp_stable)



print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)
