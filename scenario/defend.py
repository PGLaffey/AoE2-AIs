from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation, ButtonLocation
from AoE2ScenarioParser.objects.data_objects.variable import Variable
from AoE2ScenarioParser.objects.support.enums.group_by import GroupBy
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.trigger_lists.attribute import Attribute

input_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend.aoe2scenario'
output_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend - Python.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)

t_man = scenario.trigger_manager

xs_manager = scenario.xs_manager
xs_manager.xs_check.raise_on_error = True
xs_manager.xs_check.ignores.add('DiscardedFn')
xs_manager.xs_check.ignores.add('NoNumPromo')
xs_manager.initialise_xs_trigger(insert_index=0)
xs_manager.add_script(xs_file_path='../xs/defend.xs', validate=True)

players = [PlayerId.ONE.value, PlayerId.TWO.value, PlayerId.THREE.value]


for player in players:
    # Reset Hero Tree
    reset_hero_trigger = t_man.add_trigger(f'Reset Heroes (p{player})')
    reset_hero_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
                                                             object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                             button_location=ButtonLocation.r3c1)
    reset_hero_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
                                                         quantity=TechInfo.ILLUMINATION.ICON_ID)
    reset_hero_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
                                                         message='Reset Hero Tree')
    reset_hero_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
                                                                message='Reset Hero Tree <cost>')
    reset_hero_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
                                                             quantity=1000)
    reset_hero_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_0.ID,
                                                            enabled=True)

    # Research Defense Tech
    defense_tech_count = 10
    defense_tech_trigger = t_man.add_trigger(f'Setup Defense Tech (p{player})')
    defense_tech_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                               object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                               button_location=ButtonLocation.r2c1)
    defense_tech_trigger.new_effect.change_technology_cost(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                           resource_1=Attribute.STONE_STORAGE, resource_1_quantity=500,
                                                           resource_2=Attribute.WOOD_STORAGE, resource_2_quantity=500)
    defense_tech_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                           quantity=TechInfo.MURDER_HOLES.ICON_ID)
    defense_tech_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                           message='Research Defense Technology')
    defense_tech_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                                  message='Research Defense Technology <cost>')
    defense_tech_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                               quantity=defense_tech_count)
    defense_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                              enabled=True)

    do_defense_tech_trigger = t_man.add_trigger(f'Do Defense Tech (p{player})', looping=True)
    do_defense_tech_trigger.new_condition.research_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID)
    do_defense_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_1.ID,
                                                              enabled=True)
    do_defense_tech_trigger.new_effect.send_chat(source_player=player, message=f'Do Defense Tech')


    # Research Unit Tech
    unit_tech_count = 10
    unit_tech_trigger = t_man.add_trigger(f'Setup unit Tech (p{player})')
    unit_tech_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                               object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                               button_location=ButtonLocation.r2c2)
    unit_tech_trigger.new_effect.change_technology_cost(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                           resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=500,
                                                           resource_2=Attribute.GOLD_STORAGE, resource_2_quantity=500)
    unit_tech_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                           quantity=TechInfo.HAND_CANNON.ICON_ID)
    unit_tech_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                           message='Research Unit Technology')
    unit_tech_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                                  message='Research Unit Technology <cost>')
    unit_tech_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                               quantity=unit_tech_count)
    unit_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_2.ID,
                                                              enabled=True)

    # Research Eco Tech
    eco_tech_count = 10
    eco_tech_trigger = t_man.add_trigger(f'Setup Eco Tech (p{player})')
    eco_tech_trigger.new_effect.change_technology_location(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                               object_list_unit_id_2=BuildingInfo.HALL_OF_HEROES.ID,
                                                               button_location=ButtonLocation.r2c3)
    eco_tech_trigger.new_effect.change_technology_cost(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                           resource_1=Attribute.FOOD_STORAGE, resource_1_quantity=500,
                                                           resource_2=Attribute.WOOD_STORAGE, resource_2_quantity=500)
    eco_tech_trigger.new_effect.change_technology_icon(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                           quantity=TechInfo.HERBAL_MEDICINE.ICON_ID)
    eco_tech_trigger.new_effect.change_technology_name(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                           message='Research Eco Technology')
    eco_tech_trigger.new_effect.change_technology_description(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                                  message='Research eco Technology <cost>')
    eco_tech_trigger.new_effect.enable_technology_stacking(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                               quantity=eco_tech_count)
    eco_tech_trigger.new_effect.enable_disable_technology(source_player=player, technology=TechInfo.BLANK_TECHNOLOGY_3.ID,
                                                              enabled=True)




print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)