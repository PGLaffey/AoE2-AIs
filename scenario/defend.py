from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.heroes import HeroInfo
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation
from AoE2ScenarioParser.objects.data_objects.variable import Variable
from AoE2ScenarioParser.objects.support.enums.group_by import GroupBy
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

input_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend.aoe2scenario'
output_path = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario/Defend - Python.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)

t_man = scenario.trigger_manager

xs_manager = scenario.xs_manager
xs_manager.xs_check.raise_on_error = True
xs_manager.xs_check.ignores.add('DiscardedFn')
xs_manager.xs_check.ignores.add('NoNumPromo')
xs_manager.initialise_xs_trigger(insert_index=0)
xs_manager.add_script(xs_file_path='C:\\Program Files (x86)\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\xs\\defend.xs', validate=True)

trigger_event_var = 10
# Trigger Event 2
event2 = t_man.add_trigger(name='Event 2 - Sappers')
event2.new_condition.variable_value(variable=trigger_event_var, comparison=Comparison.EQUAL, quantity=2)
event2.new_effect.change_variable(variable=trigger_event_var, operation=Operation.SET, quantity=0)



print(t_man.get_summary_as_string())
q = input('Save?')
if q.lower() == 'y' or q.lower() == 'yes':
    scenario.write_to_file(output_path)