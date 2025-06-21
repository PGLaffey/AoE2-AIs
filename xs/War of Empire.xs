// Town Variable IDs (10 x town_number + ID)
// e.g. Town 3 Defense Level = 10 x 3 + 2 = Var 32
const int var_town_owner = 0;
const int var_town_eco_level = 1;
const int var_town_defense_level = 2;
const int var_town_resource = 3;
const int var_town_new_owner = 4;
const int var_town_center_x = 5;
const int var_town_center_y = 6;
const int var_town_rebuild = 7;

const int town_count = 10;

int town_var_id(int town_num = 0, int var = 0) {
    return ((town_num * 10) + var);
}

void init_towns() {
    for (i = 0; < town_count) {
        xsSetTriggerVariable(town_var_id(i, var_town_owner), 7);
        xsSetTriggerVariable(town_var_id(i, var_town_eco_level), 1);
        xsSetTriggerVariable(town_var_id(i, var_town_defense_level), 1);
        int resource_type = 0;
        switch (i) {
            case 1: {
                resource_type = cAttributeFoodGeneration;
            }
            case 2: {
                resource_type = cAttributeWoodGeneration;
            }
            case 3: {
                resource_type = cAttributeGoldGeneration;
            }
            case 4: {
                resource_type = cAttributeStoneGeneration;
            }
            default: {
                resource_type = cAttributeFoodGeneration;
            }
        }
        xsSetTriggerVariable(town_var_id(i, var_town_resource), resource_type);
        xsSetTriggerVariable(town_var_id(i, var_town_rebuild), 1);
    }
}

int get_town_level(int town_num = 0, int type = 0) {
    if (town_num == 0 || type == 0) {
        return (0);
    }
    int town_level_var_id = (town_num * 10) + type;
    return xsTriggerVariable(town_level_var_id);
}

int change_town_level(int town_num = 0, int type = 0, bool up = true) {
    int town_level = get_town_level(town_num, type);
    if (up) {
        town_level = town_level + 1;
    } else if (town_level > 0) {
        town_level = town_level - 1;
    } 
    xsSetTriggerVariable(town_level_var_id, town_level);
    xsChatData("Town " + town_num + " changed " + type + " to level " + town_level);
    return (town_level);
}

void change_town_eco_level(int town_num = 0, bool up = true) {
    int town_level = get_town_level(town_num, var_town_eco_level);
    int town_resource = get_town_level(town_num, var_town_resource);
    int town_owner = get_town_level(town_num, var_town_owner);
    xsEffectAmount(cModResource, town_resource, cAttributeAdd, (town_level * 100 * -1), town_owner);
    int new_town_level = change_town_level(town_num, var_town_eco_level, up);
    xsEffectAmount(cModResource, town_resource, cAttributeAdd, (new_town_level * 100), town_owner);
    xsChatData("Player " + town_owner + " resource " + town_resource + " changed by " + (new_town_level - town_level));
}

void change_town_defense_level(int town_num = 0, bool up = true) {
    int new_town_level = change_town_level(town_num, var_town_defense_level, up);
    xsChatData("Town " + town_num + "defense changed to " + new_town_level);
}

void change_town_owner(int town_num = 0) {
    int new_owner = xsTriggerVariable(var_town_new_owner);
    if (new_owner == 0 or town_num == 0) {
        return ()
    }
    // Remove income from current owner
    int town_eco_level = get_town_level(town_num, var_town_eco_level);
    int town_resource = get_town_level(town_num, var_town_resource);
    int town_owner = get_town_level(town_num, var_town_owner);
    xsEffectAmount(cModResource, town_resource, cAttributeAdd, (town_eco_level * 100 * -1), town_owner);
    // Add income to new owner
    xsEffectAmount(cModResource, town_resource, cAttributeAdd, (town_eco_level * 100), new_owner);
    // Change current owner to new owner
    xsSetTriggerVariable(town_var_id(town_num, var_town_owner), new_owner);
    xsSetTriggerVariable(town_var_id(town_num, var_town_new_owner), 0);
    // Remove a town level as damage
    change_town_eco_level(town_num, false);
    change_town_defense_level(town_num, false);
    // Create center tower
    // TODO create center tower with ability to rebuild
    xsChatData("Town " + town_num + " ownership changed from " + town_owner + " to " + new_owner);
 }

int roll_dice(int dice_no = 0, int sides = 1) {
    int num = xsGetRandomNumberMax(sides) + 1;
    xsSetTriggerVariable(dice_no, num);
    return (num);
}

// Town Upgrade Eco Triggers
void town_1_up_eco() {
    change_town_eco_level(1);
}

void town_2_up_eco() {
    change_town_eco_level(2);
}

void town_3_up_eco() {
    change_town_eco_level(3);
}

void town_4_up_eco() {
    change_town_eco_level(4);
}

void town_5_up_eco() {
    change_town_eco_level(5);
}

void town_6_up_eco() {
    change_town_eco_level(6);
}

void town_7_up_eco() {
    change_town_eco_level(7);
}

void town_8_up_eco() {
    change_town_eco_level(8);
}

void town_9_up_eco() {
    change_town_eco_level(9);
}

void town_10_up_eco() {
    change_town_eco_level(10);
}

// Town Upgrade Defense Triggers
void town_1_up_defense() {
    change_town_defense_level(1);
}

void town_2_up_defense() {
    change_town_defense_level(2);
}

void town_3_up_defense() {
    change_town_defense_level(3);
}

void town_4_up_defense() {
    change_town_defense_level(4);
}

void town_5_up_defense() {
    change_town_defense_level(5);
}

void town_6_up_defense() {
    change_town_defense_level(6);
}

void town_7_up_defense() {
    change_town_defense_level(7);
}

void town_8_up_defense() {
    change_town_defense_level(8);
}

void town_9_up_defense() {
    change_town_defense_level(9);
}

void town_10_up_defense() {
    change_town_defense_level(10);
}

// Town Change Ownership Triggers
void town_1_change_ownership() {
    change_town_owner(1);
}

void town_2_change_ownership() {
    change_town_owner(2);
}

void town_3_change_ownership() {
    change_town_owner(3);
}

void town_4_change_ownership() {
    change_town_owner(4);
}

void town_5_change_ownership() {
    change_town_owner(5);
}

void town_6_change_ownership() {
    change_town_owner(6);
}

void town_7_change_ownership() {
    change_town_owner(7);
}

void town_8_change_ownership() {
    change_town_owner(8);
}

void town_9_change_ownership() {
    change_town_owner(9);
}

void town_10_change_ownership() {
    change_town_owner(10);
}
