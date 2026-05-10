FER_MODEL = "affectnet"

LIFT_LEFT_LEG_GOAL_REPETITION = 5
LIFT_RIGHT_LEG_GOAL_REPETITION = 5
FOREFOOTING_ON_CHAIR_REPETITION = 5
FOREFOOTING_ARM_RAISING_REPETITION = 1

SADANIE_NA_STOLICKU_REPETITION_SCORE = 1
FOREFOOTING_VEDLA_TELA_REPETITION = 1
FOREFOOTING_IN_LYING_REPETITION = 1
SIT_STAND_RAISE_ARMS_GOAL_REPETITION = 1
FOREFOOTING_RUKY_NAD_HLAVU_REPETITION = 1


# Cviky na experiment
ARM_CIRCLING = 5

TPOSE_GOAL_REPETITION_COUNT = 5
PREDPAZOVANIE = 5
FOREFOOTING_PREDPAZOVANIE_REPETITION = 5
FOREFOOTING_ROZPAZOVANIE_REPETITION = 5
SQUAT_GOAL_REPETITION_SCORE = 5
KRIZNY_FOREFOOTING_IN_LYING_REPETITION = 5


EXERCISE_MESSAGES = {
    # Sadanie a vstavanie zo stolicky
     "chair_circling": {
        "start_msg": "00chair_circling_start",
        "end_msg": "00chair_circling_end",
        "note": "Cvi\u010denie 1 - Obchadzanie stolicky",
        "sound": "sounds/Začíname cvičiť, prvý cvik, sadanie a vstávanie zo stoličky.wav",
        "score_limit": ARM_CIRCLING,
        "checker": "chair_circling_exercise",
        "updater": "update_score_chair_circling",
        "name": "chair_circling"
    },
     "arm_sit_circling": {
        "start_msg": "00arm_sit_circling_start",
        "end_msg": "00arm_sit_circling_end",
        "note": "Cvi\u010denie 1 - Kruzenie rukamy v sede",
        "sound": "sounds/Začíname cvičiť, prvý cvik, sadanie a vstávanie zo stoličky.wav",
        "score_limit": ARM_CIRCLING,
        "checker": "arm_sit_circling_exercise",
        "updater": "update_score_arm_circling",
        "name": "arm_sit_circling"
    },
    "arm_circling": {
        "start_msg": "00arm_circling_start",
        "end_msg": "00arm_circling_end",
        "note": "Cvi\u010denie 1 - Kruzenie rukamy",
        "sound": "sounds/Začíname cvičiť, prvý cvik, sadanie a vstávanie zo stoličky.wav",
        "score_limit": ARM_CIRCLING,
        "checker": "arm_circling_exercise",
        "updater": "update_score_arm_circling",
        "name": "arm_circling"
    },
    "squat": {
        "start_msg": "00squat_start",
        "end_msg": "00squat_end",
        "note": "Cvi\u010denie 1 - Drepy",
        "sound": "sounds/Začíname cvičiť, prvý cvik, sadanie a vstávanie zo stoličky.wav",
        "score_limit": SQUAT_GOAL_REPETITION_SCORE,
        "checker": "squat_exercise",
        "updater": "update_score_squat",
        "name": "squat"
    },
    "sadanie_na_stolicku": {
        "start_msg": "00sadanie_na_stolicku_start",
        "end_msg": "00sadanie_na_stolicku_end",
        "note": "Sadanie na stoličku",
        "sound": "",
        "score_limit": SADANIE_NA_STOLICKU_REPETITION_SCORE,
        "checker": "sadanie_na_stolicku_exercise",
        "updater": "update_score_sadanie_na_stolicku",
        "name": "sadanie_na_stolicku"
    },
    # Rozpazovanie
    "tpose": {
        "start_msg": "00tpose_start",
        "end_msg": "00tpose_end",
        "note": "Cvičenie - upažovanie",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": TPOSE_GOAL_REPETITION_COUNT,
        "checker": "tpose_exercise",
        "updater": "update_score_tpose",
        "name": "tpose"
    },
    "lift_left_leg": {
        "start_msg": "00lift_left_leg_start",
        "end_msg": "00lift_left_leg_end",
        "note": "CVIK 3 - ZDVIHNANIE LAVEJ NOHY",
        "sound": "sounds/Prejdite-na-cvik-dva_-dvíhanie-kolien.wav",
        "score_limit": LIFT_LEFT_LEG_GOAL_REPETITION,
        "checker": "lift_left_leg_exercise",
        "updater": "update_score_lift_left_leg",
        "name": "lift_left_leg"
    },
    "lift_right_leg": {
        "start_msg": "00lift_right_leg_start",
        "end_msg": "00lift_right_leg_end",
        "note": "CVIK 4 - ZDVIHNANIE PRAVEJ NOHY",
        "sound": "sounds/Teraz-vymeňte-strany.wav",
        "score_limit": LIFT_RIGHT_LEG_GOAL_REPETITION,
        "checker": "lift_right_leg_exercise",
        "updater": "update_score_lift_right_leg",
        "name": "lift_right_leg"
    },

    "sit_stand_raise_arms": {
        "start_msg": "00sit_stand_raise_arms_start",
        "end_msg": "00sit_stand_raise_arms_end,",
        "note": "Cvičenie - Vstávanie zo stoličky a vzpažovanie",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": SIT_STAND_RAISE_ARMS_GOAL_REPETITION,
        "checker": "sit_stand_raise_arms_exercise",
        "updater": "update_score_sit_stand_raise_arms",
        "name": "sit_stand_raise_arms"
    },
    "TODO_chodza_okolo_stolicky": {

    },
    "forefooting_on_chair": {
        "start_msg": "00forefooting_on_chair_start",
        "end_msg": "00forefooting_on_chair_end,",
        "note": "Cvičenie - Prednožovanie v sede",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": FOREFOOTING_ON_CHAIR_REPETITION,
        "checker": "forefooting_on_chair_exercise",
        "updater": "update_score_forefooting_on_chair",
        "name": "forefooting_on_chair"
    },
    "forefooting_arm_raising": {
        "start_msg": "00forefooting_arm_raising_start",
        "end_msg": "00forefooting_arm_raising_end,",
        "note": "Cvičenie - Prednožovanie so zdvíhaním rúk",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": FOREFOOTING_ARM_RAISING_REPETITION,
        "checker": "forefooting_arm_raising_exercise",
        "updater": "update_score_forefooting_arm_raising",
        "name": "forefooting_arm_raising"
    },
    "forefooting_in_lying": {
        "start_msg": "00forefooting_in_lying_start",
        "end_msg": "00forefooting_in_lying_end,",
        "note": "Cvičenie - Prednožovanie v ľahu",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": FOREFOOTING_IN_LYING_REPETITION,
        "checker": "forefooting_in_lying_exercise",
        "updater": "update_score_forefooting_in_lying",
        "name": "forefooting_in_lying"
    },
    "krizny_forefooting_in_lying": {
        "start_msg": "00krizny_forefooting_in_lying_start",
        "end_msg": "00krizny_forefooting_in_lying_end,",
        "note": "Cvičenie - Prednožovanie do kríža v ľahu",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": KRIZNY_FOREFOOTING_IN_LYING_REPETITION,
        "checker": "krizny_forefooting_in_lying_exercise",
        "updater": "update_score_krizny_forefooting_in_lying",
        "name": "krizny_forefooting_in_lying"
    },
    "forefooting_ruky_pri_tele": {
        "start_msg": "00forefooting_ruky_pri_tele_start",
        "end_msg": "00forefooting_ruky_pri_tele_end,",
        "note": "Prednožovanie s rukami vedľa tela",
        "sound": "sounds/Začiatok-cviku-tri_-upažovanie-rúk.wav",
        "score_limit": FOREFOOTING_VEDLA_TELA_REPETITION,
        "checker": "forefooting_ruky_pri_tele_exercise",
        "updater": "update_score_forefooting_ruky_pri_tele",
        "name": "forefooting_ruky_pri_tele"
    },
    "forefooting_ruky_nad_hlavu": {
        "start_msg": "00forefooting_ruky_nad_hlavu_start",
        "end_msg": "00forefooting_ruky_nad_hlavu_end,",
        "note": "Prednožovanie s rukami nad hlavou",
        "sound": "",
        "score_limit": FOREFOOTING_RUKY_NAD_HLAVU_REPETITION,
        "checker": "forefooting_ruky_nad_hlavu_exercise",
        "updater": "update_score_forefooting_ruky_nad_hlavu",
        "name": "forefooting_ruky_nad_hlavu"
    },
    "forefooting_predpazovanie": {
        "start_msg": "00forefooting_predpazovanie_start",
        "end_msg": "00forefooting_predpazovanie_end,",
        "note": "Prednožovanie s predpažovaním",
        "sound": "",
        "score_limit": FOREFOOTING_PREDPAZOVANIE_REPETITION,
        "checker": "forefooting_predpazovanie_exercise",
        "updater": "update_score_forefooting_predpazovanie",
        "name": "forefooting_predpazovanie"
    },
    "forefooting_rozpazovanie": {
        "start_msg": "00forefooting_rozpazovanie_start",
        "end_msg": "00forefooting_rozpazovanie_end,",
        "note": "Prednožovanie s rozpažovaním",
        "sound": "",
        "score_limit": FOREFOOTING_ROZPAZOVANIE_REPETITION,
        "checker": "forefooting_rozpazovanie_exercise",
        "updater": "update_score_forefooting_rozpazovanie",
        "name": "forefooting_rozpazovanie"
    },
    "predpazovanie": {
        "start_msg": "00predpazovanie_start",
        "end_msg": "00predpazovanie_end,",
        "note": "Predpažovanie",
        "sound": "",
        "score_limit": PREDPAZOVANIE,
        "checker": "predpazovanie_exercise",
        "updater": "update_score_predpazovanie",
        "name": "predpazovanie"
    },
    
}