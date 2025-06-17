const int var_event_type_dice = 0;
const int var_player_dice = 1;
const int var_side_dice = 2;
const int var_event_dice = 3;
const int var_quantity_dice = 4;

const int var_trigger_event = 10;

int test = 0;
int attack_unique_techs = 0;
int attack_unique_techs_status = 0;

void roll_all_dice() {
    for (var = 0; < 10) {
        int sides = 1000;
        if(xsTriggerVariable(var) < 0) {
            sides = xsTriggerVariable(var) * -1;
        }
        int num = xsGetRandomNumberMax(sides) + 1;
        xsChatData("Set Dice "+var+1+" to "+num+" out of "+sides);
        xsSetTriggerVariable(var, num);
    }
}

int roll_dice(int dice_no = 0, int sides = 1) {
    int num = xsGetRandomNumberMax(sides) + 1;
    xsSetTriggerVariable(dice_no, num);
    return (num);
}

void roll_dice_unused(int dice_no = 0) {
    int sides = 1000;
    if(xsTriggerVariable(dice_no) < 0) {
        sides = xsTriggerVariable(dice_no) * -1;
    }
    int num = xsGetRandomNumberMax(sides) + 1;
    xsSetTriggerVariable(dice_no, num);
}

// ===== Common Defend Events =====
int set_defend_unique_techs() {
    int list = xsArrayCreateInt(54, 0, "defend_unique_techs");
    xsArraySetInt(list, 0, 912); // Feteters
    xsArraySetInt(list, 1, 460); // Atlatl
    xsArraySetInt(list, 2, 24); // Garland Wars
    xsArraySetInt(list, 3, 834); // Mahayana
    xsArraySetInt(list, 4, 578); // Kabash
    xsArraySetInt(list, 5, 3); // Yeomen  
    xsArraySetInt(list, 6, 685); // Stirrups 
    xsArraySetInt(list, 7, 686); // Bagains
    xsArraySetInt(list, 8, 754); // Burgundian Vineyards
    xsArraySetInt(list, 9, 627); // Manipur Cavalry
    xsArraySetInt(list, 10, 482); // Stronghold
    xsArraySetInt(list, 11, 5); // Furor Celtica
    xsArraySetInt(list, 12, 462); // Great Wall
    xsArraySetInt(list, 13, 690); // Cuman Mercenaries
    xsArraySetInt(list, 14, 832); // Wootz Steel
    xsArraySetInt(list, 15, 923); // Svan Towers
    xsArraySetInt(list, 16, 924); // Aznauri Cavalry
    xsArraySetInt(list, 17, 835); // Kshatriyas
    xsArraySetInt(list, 18, 506); // Grant Trunk Road
    xsArraySetInt(list, 19, 507); // Shatangi
    xsArraySetInt(list, 20, 516); // Andean Sling
    xsArraySetInt(list, 21, 499); // Silk Road
    xsArraySetInt(list, 22, 494); // Pirotechnia
    xsArraySetInt(list, 23, 484); // Yasama
    xsArraySetInt(list, 24, 996); // Fortified Bastions
    xsArraySetInt(list, 25, 1006); // Lamellar Armor
    xsArraySetInt(list, 26, 1007); // Ordo Cavalry
    xsArraySetInt(list, 27, 486); // Eupseong
    xsArraySetInt(list, 28, 692); // Tower Shields
    xsArraySetInt(list, 29, 515); // Recurve Bow
    xsArraySetInt(list, 30, 625); // Forced Levy
    xsArraySetInt(list, 31, 577); // Farimba
    xsArraySetInt(list, 32, 485); // Hulche Javelineers
    xsArraySetInt(list, 33, 7); // Citadels
    xsArraySetInt(list, 34, 783); // Lechitic Legacy
    xsArraySetInt(list, 35, 573); // Arquebus
    xsArraySetInt(list, 36, 883); // Ballistas
    xsArraySetInt(list, 37, 884); // Comitatenses
    xsArraySetInt(list, 38, 28); // Birmaristan
    xsArraySetInt(list, 39, 1070); // Coiled Serpent Array
    xsArraySetInt(list, 40, 1069); // Bolt Magazine
    xsArraySetInt(list, 41, 757); // Hauberk
    xsArraySetInt(list, 42, 455); // Detinets
    xsArraySetInt(list, 43, 513); // Druzhina
    xsArraySetInt(list, 44, 440); // Supremacy
    xsArraySetInt(list, 45, 687); // Silk Armor
    xsArraySetInt(list, 46, 11); // Crenellations
    xsArraySetInt(list, 47, 491); // Sipahi
    xsArraySetInt(list, 48, 10); // Artillery
    xsArraySetInt(list, 49, 629); // Paper Money
    xsArraySetInt(list, 50, 463); // Chieftains
    xsArraySetInt(list, 51, 49); // Bigsveigar
    xsArraySetInt(list, 52, 1061); // Tuntian
    xsArraySetInt(list, 53, 1062); // Ming Guang Armor                 
    return (list);
}

void re_attack_unique_tech(int tech_index = 0, int player = 0) {
    int status = xsArrayGetInt(attack_unique_techs_status, tech_index);
    int tech_id = xsArrayGetInt(attack_unique_techs, tech_index);
    switch (player) {
        case 1 : {
            if (status % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(attack_unique_techs_status, tech_index, status + 1);
            }
        }
        case 2 : {
            if (status / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(attack_unique_techs_status, tech_index, status + 2);
            }
        }
        case 3 : {
            if (status / 2 / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(attack_unique_techs_status, tech_index, status + 4);
            }
        }
        case 4 : {
            if (status / 2 / 2 / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(attack_unique_techs_status, tech_index, status + 8);
            }
        }
    }
}
// ===== (END) Common Defend Events =====

// ===== Common Attack Events =====
void re_cavalry_armor(int player = 0) {
    xsResearchTechnology(80, false, true, player);
    xsResearchTechnology(82, false, true, player); 
    xsResearchTechnology(81, false, true, player); 
}

void re_infantry_armor(int player = 0) {
    xsResearchTechnology(77, false, true, player);
    xsResearchTechnology(76, false, true, player); 
    xsResearchTechnology(74, false, true, player); 
}

void re_archer_armor(int player = 0) {
    xsResearchTechnology(219, false, true, player);
    xsResearchTechnology(212, false, true, player); 
    xsResearchTechnology(211, false, true, player); 
}

void re_archer_attack(int player = 0) {
    xsResearchTechnology(201, false, true, player); // Bracer
    xsResearchTechnology(200, false, true, player); // Bodkin Arrow
    xsResearchTechnology(199, false, true, player); // Fletching
}

void re_melee_attack (int player = 0) {
    xsResearchTechnology(75, false, true, player); // Blast Furnace
    xsResearchTechnology(68, false, true, player); // Iron Casting
    xsResearchTechnology(67, false, true, player); // Forging Furnace
}
// ===== (END) Common Attack Events =====

// ===== Common Neutral Events =====
void spawn_deer() {
    int quantity = roll_dice(var_quantity_dice, 50);
    xsEffectAmount(cGaiaModResource, cAttributeSpawnCap, cAttributeSet, 15);
    xsEffectAmount(cGaiaSpawnUnit, 65, 109, quantity);
    xsChatData("Spring has come and the deer flourish");
}
// ===== (END) Common Neutral Events =====

void do_common_attack_event() {
    int player = roll_dice(var_player_dice, 4) + 3;
    int event = roll_dice(var_event_dice, 5);
    switch(event) {
        case 1 : {
            re_melee_attack(player);
        }
        case 2 : {
            re_infantry_armor(player); 
        }
        case 3 : {
            re_cavalry_armor(player);
        }
        case 4 : {
            re_archer_attack(player);
        }
        case 5 : {
            re_archer_armor(player);
        }
    }
}

void do_common_defend_event() {
    int player = roll_dice(var_player_dice, 3);
    int event = roll_dice(var_event_dice, 55);
    if (event <= xsArrayGetSize(attack_unique_techs)) {
        re_attack_unique_tech(event, player);
    } else {
        switch(event - xsArrayGetSize(attack_unique_techs)) {
            case 1 : {
                xsChatData("Event 55");
            }
        }
    }
}

void do_common_neutral_event() {
    int event = roll_dice(var_event_dice, 2);
    switch(event) {
        case 1 : {
            spawn_deer();
        }
        case 2 : {
            xsSetTriggerVariable(var_trigger_event, 1);
            xsChatData("Winter has come and hungry wolves decend the mountains");
        }
    }
}

void do_common_event() {
    int side = roll_dice(var_side_dice, 3);
    switch(side) {
        case 1 : {
            do_common_attack_event();
        }
        case 2 : {
            do_common_defend_event();
        }
        case 3 : {
            do_common_neutral_event();
        }
        default : {
            xsChatData("Invalid roll "+side+" for Side Dice");
        }
    }
}

void event_roll() {
    // xsSetTriggerVariable(var_event_dice, -10000); // Event Chance
    // xsSetTriggerVariable(var_player_dice, -4); // Player select
    // xsSetTriggerVariable(var_side_dice, -2); // Side select

    // roll_dice();
    int event_type = roll_dice(var_event_type_dice, 100);
    if (event_type == 100) {
        do_common_event();
    }
    roll_dice_unused(4);
    roll_dice_unused(5);
    roll_dice_unused(6);
    roll_dice_unused(7);
    roll_dice_unused(8);
    roll_dice_unused(9);
}

void main() {
    test = xsArrayCreateInt(5, 0, "test");
    attack_unique_techs = set_defend_unique_techs();
    attack_unique_techs_status = xsArrayCreateInt(xsArrayGetSize(attack_unique_techs), 0, "attack_unique_tech_status");
}