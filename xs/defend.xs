const int var_event_type_dice = 0;
const int var_player_dice = 1;
const int var_side_dice = 2;
const int var_event_dice = 3;
const int var_quantity_dice = 4;

const int var_trigger_event = 10;

int test = 0;
int defend_unique_techs = 0;
int defend_unique_techs_desc = 0;
int defend_unique_techs_status = 0;

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
    xsArraySetInt(list, 54, 488); // Kamandaran
    xsArraySetInt(list, 55, 782); // Szlachta Privileges
    return (list);
}
int set_defend_unique_techs_descriptions() {
    int list = xsArrayCreateString(54, 0, "defend_unique_techs_desc");
    xsArraySetString(list, 0, "Fereters: Infantry +30 HP"); // Feteters
    xsArraySetString(list, 1, "Atlatl: Skirmishers +1 attack and range"); // Atlatl
    xsArraySetString(list, 2, "Garland Wars: Infantry units: +4 attack"); // Garland Wars
    xsArraySetString(list, 3, "Mahayana: Villagers and Monks take -10% Population space"); // Mahayana
    xsArraySetString(list, 4, "Kasbah: Castles: +25% team work speed"); // Kabash
    xsArraySetString(list, 5, "Yeomen	Foot archers: +1 range and Towers: +2 attack"); // Yeomen
    xsArraySetString(list, 6, "Stirrups	Cavalry units: +33% attack speed"); // Stirrups
    xsArraySetString(list, 7, "Bagains	Two-Handed Swordsman: +5 melee armor"); // Bagains
    xsArraySetString(list, 8, "Burgundian Vineyards	Villagers generate 0.017 gold per second while working on Farms"); // Burgundian Vineyards
    xsArraySetString(list, 9, "Manipur Cavalry	Cavalry units: +4 attack against archers"); // Manipur Cavalry
    xsArraySetString(list, 10, "Stronghold	Castles and Towers: +33% attack speed and Castles heal 30 hit points per minute for allied infantry in a 7 tile radius"); // Stronghold
    xsArraySetString(list, 11, "Furor Celtica	Siege Workshop units: +40% hit points"); // Furor Celtica
    xsArraySetString(list, 12, "Great Wall	Walls and towers: +30% hit points"); // Great Wall
    xsArraySetString(list, 13, "Cuman Mercenaries	Allied players can train up to 5 free Elite Kipchaks per Castle"); // Cuman Mercenaries
    xsArraySetString(list, 14, "Wootz Steel	Infantry and cavalry units ignore armor"); // Wootz Steel
    xsArraySetString(list, 15, "Svan Towers	Defensive buildings +2 attack; Towers fire arrows that pierce multiple units"); // Svan Towers
    xsArraySetString(list, 16, "Aznauri Cavalry	Cavalry units take 15% less population space"); // Aznauri Cavalry
    xsArraySetString(list, 17, "Kshatriyas	Military units cost -25% food"); // Kshatriyas
    xsArraySetString(list, 18, "Grand Trunk Road	+10% gold gather speed from all sources (Gold Mines, trade, and Relics) and Trading fee reduced to 10%"); // Grant Trunk Road
    xsArraySetString(list, 19, "Shatagni	Hand Cannoneers: +2 range"); // Shatangi
    xsArraySetString(list, 20, "Andean Sling	Minimum range of Skirmishers and Slingers removed and Slingers: +1 attack"); // Andean Sling
    xsArraySetString(list, 21, "Silk Road	Trade Cart and Trade Cog cost -50%"); // Silk Road
    xsArraySetString(list, 22, "Pirotechnia	Hand Cannoneer: +15% pass-through damage, 90% accurate"); // Pirotechnia
    xsArraySetString(list, 23, "Yasama	Towers fire 2 additional arrows"); // Yasama
    xsArraySetString(list, 24, "Fortified Bastions	Castles, Town Centers, walls, gates, and towers to regenerate 500 hit points per minute."); // Fortified Bastions
    xsArraySetString(list, 25, "Lamellar Armor	Infantry and Skirmishers reflect 25% melee damage back to the attacker"); // Lamellar Armor
    xsArraySetString(list, 26, "Ordo Cavalry	Cavalry regenerates HP in combat"); // Ordo Cavalry
    xsArraySetString(list, 27, "Eupseong	Watch Tower-line: +2 range"); // Eupseong
    xsArraySetString(list, 28, "Tower Shields	Spearman-line and Skirmishers: +2 pierce armor"); // Tower Shields
    xsArraySetString(list, 29, "Recurve Bow	Mounted archers: +1 attack and range"); // Recurve Bow
    xsArraySetString(list, 30, "Forced Levy	Militia-line costs +20 food, -20 gold"); // Forced Levy
    xsArraySetString(list, 31, "Farimba	Cavalry units: +5 attack"); // Farimba
    xsArraySetString(list, 32, "Hul'che Javelineers	Skirmishers throw extra spear that deals 1 damage"); // Hulche Javelineers
    xsArraySetString(list, 33, "Citadels	Castles +4 pierce attack, +3 attack vs rams, +3 attack vs infantry, receive -25% bonus damage"); // Citadels
    xsArraySetString(list, 34, "Lechitic Legacy	Scout-line have +0.5 blast radius [33% effect]"); // Lechitic Legacy
    xsArraySetString(list, 35, "Arquebus	Improved gunpowder unit accuracy against moving targets and +0.5 gunpowder projectile speed, +0.2 for Bombard Cannon and Bombard Tower"); // Arquebus
    xsArraySetString(list, 36, "Ballistas	Scorpions: +33% attack speed and Galley-line: +2 attack"); // Ballistas
    xsArraySetString(list, 37, "Comitatenses	Militia-line, Knight-line, and Centurions train 50% faster and receive +5 charge attack."); // Comitatenses
    xsArraySetString(list, 38, "Bimaristan	Monks automatically heal multiple nearby units."); // Birmaristan
    xsArraySetString(list, 39, "Coiled Serpent Array	Spearman-line and White Feather Guards gain additional HP when near each other."); // Coiled Serpent Array
    xsArraySetString(list, 40, "Bolt Magazine	Archer-line, War Chariots and Lou Chuans fire additional projectiles"); // Bolt Magazine
    xsArraySetString(list, 41, "Hauberk	Knight-line: +1/+2 armor"); // Hauberk
    xsArraySetString(list, 42, "Detinets	Replaces 40% of Castles' and towers' stone cost with wood"); // Detinets
    xsArraySetString(list, 43, "Druzhina	Infantry units have +0.5 blast radius [+5 effect]"); // Druzhina
    xsArraySetString(list, 44, "Supremacy	Villagers: +6 attack, +2/+2 armor, and +40 hit points"); // Supremacy
    xsArraySetString(list, 45, "Silk Armor	Scout-line, Steppe Lancer, and mounted archers: +1/+1 armor"); // Silk Armor
    xsArraySetString(list, 46, "Crenellations	Castles: +3 range and Garrisoned infantry fire arrows"); // Crenellations
    xsArraySetString(list, 47, "Sipahi	Mounted archers: +20 hit points"); // Sipahi
    xsArraySetString(list, 48, "Artillery	Bombard Tower, Bombard Cannon, and Cannon Galleon: +2 range"); // Artillery
    xsArraySetString(list, 49, "Paper Money	Villagers generate 0.014 gold per second while gathering wood"); // Paper Money
    xsArraySetString(list, 50, "Chieftains	Infantry: +5 attack against cavalry units, +4 against camel units, and generate 5 gold when killing Villagers, 20 gold when killing trade units and Monks"); // Chieftains
    xsArraySetString(list, 51, "Bogsveigar	Archer-line and Longboats: +1 attack"); // Bigsveigar
    xsArraySetString(list, 52, "Tuntian	Soldiers passively produce food"); // Tuntian
    xsArraySetString(list, 53, "Ming Guang Armor	Cavalry +2 attack vs. Siege Weapons"); // Ming Guang Armor
    xsArraySetString(list, 54, "Kamandaran	Archer-line costs 60 wood instead of 25 wood, 45 gold"); // Kamandaran
    xsArraySetString(list, 55, "Szlachta Privileges	Knight-line costs -60% gold"); // Szlachta Privileges
    return (list);
}

void re_defend_unique_tech(int tech_index = 0, int player = 0) {
    int status = xsArrayGetInt(defend_unique_techs_status, tech_index);
    int tech_id = xsArrayGetInt(defend_unique_techs, tech_index);
    string tech_desc = xsArrayGetString(defend_unique_techs_desc, int index);
    xsChatData("Player "+player+" researched "+tech_desc);
    switch (player) {
        case 1 : {
            if (status % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 1);
            }
        }
        case 2 : {
            if (status / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 2);
            }
        }
        case 3 : {
            if (status / 2 / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 4);
            }
        }
        case 4 : {
            if (status / 2 / 2 / 2 % 2 < 1) {
                xsResearchTechnology(tech_id, true, false, player);
                xsArraySetInt(defend_unique_techs_status, tech_index, status + 8);
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
    int event = roll_dice(var_event_dice, 57);
    if (event <= xsArrayGetSize(defend_unique_techs)) {
        re_defend_unique_tech(event, player);
    } else {
        switch(event - xsArrayGetSize(defend_unique_techs)) {
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
    defend_unique_techs = set_defend_unique_techs();
    defend_unique_techs_desc = set_defend_unique_techs_descriptions();
    defend_unique_techs_status = xsArrayCreateInt(xsArrayGetSize(attack_unique_techs), 0, "attack_unique_tech_status");
}