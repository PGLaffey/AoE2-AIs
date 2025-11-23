from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import Attribute, ObjectAttribute, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class A_TYPE:
    MELEE = 4
    PIERCE = 3
    INFANTRY = 1
    CAVALRY = 8
    ARCHER = 15
    BUILDING = 11
    ELEPHANT = 5
    CAMEL = 30

class AttackArmor:
    def __init__(self, attribute: ObjectAttribute, a_type: int):
        self.attribute = attribute
        self.a_type = a_type


class CustomTech:
    def __init__(self, override_tech: TechInfo.ID, name: str = None, icon: TechInfo.ICON_ID = None,
                 description: str = None, cost: list[tuple[Attribute, int]] = None, research_time: int = None,
                 stacking: int = None):
        self.override_tech = override_tech
        self.ID = override_tech
        self.name = name or 'Placeholder'
        self.icon = icon or TechInfo.SUPREMACY.ICON_ID
        self.description = f'<cost> {description or self.name}'
        self.cost = cost
        self.research_time = research_time or 30
        self.stacking = stacking
        self._applications = {}

    def add_to_building(self, player: int, building: BuildingInfo.ID, location: int, trigger: Trigger):
        params = {'source_player': player, 'technology': self.override_tech}
        trigger.new_effect.change_technology_name(**params, message=self.name)
        trigger.new_effect.change_technology_icon(**params, quantity=self.icon)
        trigger.new_effect.change_technology_research_time(**params, quantity=self.research_time)
        trigger.new_effect.change_technology_description(**params, message=self.description)
        if self.cost is not None:
            cost = {}
            for i, (resource, amount) in enumerate(self.cost):
                cost[f'resource_{i+1}'] = resource
                cost[f'resource_{i+1}_quantity'] = amount
            trigger.new_effect.change_technology_cost(**params, **cost)
        trigger.new_effect.change_technology_location(**params, object_list_unit_id_2=building, button_location=location)
        if self.stacking:
            trigger.new_effect.enable_technology_stacking(**params, quantity=self.stacking)
        if self._applications.get(player, False):
            self._applications[player].add((building, location))
        else:
            self._applications[player] = {(building, location)}
        trigger.new_effect.enable_disable_technology(**params, enabled=True)

    def update(self, player: int, trigger: Trigger, name: str = None, icon: TechInfo.ICON_ID = None,
               description: str = None, cost: list[tuple[Attribute, int]] | float = None, research_time: int = None,
               stacking: int = None):
        self.name = name or self.name
        self.icon = icon or self.icon
        if description:
            self.description = f'<cost> {description}'
        if type(cost) == float:
            self.cost = [(res, int(amount * cost)) for res, amount in self.cost]
        elif type(cost) == int:
            self.cost = [(res, cost) for res, _ in self.cost]
        else:
            self.cost = cost or self.cost
        self.research_time = research_time or self.research_time
        self.stacking = stacking or self.stacking
        for building, location in self._applications[player]:
            self.add_to_building(player, building, location, trigger)


def adjust_unit(trigger: Trigger, player: int, units: list[UnitInfo] | UnitInfo, attribute: ObjectAttribute | AttackArmor,
                quantity: int | float):
    params = {'operation': Operation.ADD if quantity > 0 else Operation.SUBTRACT}
    if type(attribute) == AttackArmor:
        params['object_attributes'] = attribute.attribute
        params['armour_attack_class'] = attribute.a_type
        params['armour_attack_quantity'] = quantity
    else:
        params['object_attributes'] = attribute
        params['quantity'] = quantity
        if attribute in [ObjectAttribute.MOVEMENT_SPEED, ObjectAttribute.ATTACK_RELOAD_TIME]:
            params['operation'] = Operation.MULTIPLY
        elif attribute in [ObjectAttribute.BLAST_ATTACK_LEVEL, ObjectAttribute.AREA_DAMAGE, ObjectAttribute.BLAST_WIDTH]:
            params['operation'] = Operation.SET
    if type(units) == UnitInfo:
        units = [units]
    for unit in units:
        trigger.new_effect.modify_attribute(source_player=player, object_list_unit_id=unit.ID, **params)

def replace_unit(trigger: Trigger, player: int, new_unit: UnitInfo, old_unit: UnitInfo, building: BuildingInfo, location: int):
    trigger.new_effect.enable_disable_object(source_player=player, object_list_unit_id=old_unit.ID, enabled=False)
    trigger.new_effect.change_train_location(source_player=player, object_list_unit_id=new_unit.ID,
                                             object_list_unit_id_2=building.ID, button_location=location)
    trigger.new_effect.enable_disable_object(source_player=player, object_list_unit_id=new_unit.ID, enabled=True)
