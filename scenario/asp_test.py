from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

scenario_folder = 'C:/Users/User/Games/Age of Empires 2 DE/76561198138036391/resources/_common/scenario'
input_path = f'{scenario_folder}/asp_test_source.aoe2scenario'
output_path = f'{scenario_folder}/asp_test_target.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_path)
scenario.write_to_file(output_path)
