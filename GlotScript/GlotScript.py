"""
Author: Amir Hossein Kargaran
Date: August, 2023

Description: This code detects/separates the script(s) (writing system(s)) of the given text.

MIT License

The base code (Meta, MIT license::permission for distribution and modification) is capable of detecting less than 40 scripts: https://github.com/facebookresearch/stopes/blob/main/stopes/pipelines/monolingual/utils/predict_script.py
The currently developed code supports all 161 Unicode 15.0 scripts.
"""

import string
import typing as tp
from collections import Counter, defaultdict
from typing import Dict, List

SCRIPT_RANGES = {
    'Adlm': [(125184, 125259), (125264, 125273), (125278, 125279)],
    'Aghb': [(66864, 66915), (66927, 66927)],
    'Ahom': [(71424, 71450), (71453, 71467), (71472, 71494)],
    'Arab': [(1536, 1540), (1542, 1547), (1549, 1562), (1564, 1566), (1568, 1599), (1601, 1648), (1649, 1756), (1758, 1791), (1872, 1919), (2160, 2193), (2199, 2273), (2275, 2303), (64336, 64829), (64832, 64975), (65008, 65023), (65136, 65140), (65142, 65276), (69216, 69246), (69314, 69319), (69328, 69336), (69370, 69375), (126464, 126467), (126469, 126495), (126497, 126498), (126500, 126500), (126503, 126503), (126505, 126514), (126516, 126519), (126521, 126521), (126523, 126523), (126530, 126530), (126535, 126535), (126537, 126537), (126539, 126539), (126541, 126543), (126545, 126546), (126548, 126548), (126551, 126551), (126553, 126553), (126555, 126555), (126557, 126557), (126559, 126559), (126561, 126562), (126564, 126564), (126567, 126570), (126572, 126578), (126580, 126583), (126585, 126588), (126590, 126590), (126592, 126601), (126603, 126619), (126625, 126627), (126629, 126633), (126635, 126651), (126704, 126705)],
    'Armi': [(67648, 67669), (67671, 67679)],
    'Armn': [(1329, 1366), (1369, 1418), (1421, 1423), (64275, 64279)],
    'Avst': [(68352, 68405), (68409, 68415)],
    'Bali': [(6912, 6988), (6990, 7039)],
    'Bamu': [(42656, 42743), (92160, 92728)],
    'Bass': [(92880, 92909), (92912, 92917)],
    'Batk': [(7104, 7155), (7164, 7167)],
    'Beng': [(2432, 2435), (2437, 2444), (2447, 2448), (2451, 2472), (2474, 2480), (2482, 2482), (2486, 2489), (2492, 2500), (2503, 2504), (2507, 2510), (2519, 2519), (2524, 2525), (2527, 2531), (2534, 2558)],
    'Berf': [(93856, 93880), (93883, 93907)],
    'Bhks': [(72704, 72712), (72714, 72758), (72760, 72773), (72784, 72812)],
    'Bopo': [(746, 747), (12549, 12591), (12704, 12735)],
    'Brah': [(69632, 69709), (69714, 69749), (69759, 69759)],
    'Brai': [(10240, 10495)],
    'Bugi': [(6656, 6683), (6686, 6687)],
    'Buhd': [(5952, 5971)],
    'Cakm': [(69888, 69940), (69942, 69959)],
    'Cans': [(5120, 5759), (6320, 6389), (72368, 72383)],
    'Cari': [(66208, 66256)],
    'Cham': [(43520, 43574), (43584, 43597), (43600, 43609), (43612, 43615)],
    'Cher': [(5024, 5109), (5112, 5117), (43888, 43967)],
    'Chrs': [(69552, 69579)],
    'Copt': [(994, 1007), (11392, 11507), (11513, 11519)],
    'Cpmn': [(77712, 77810)],
    'Cprt': [(67584, 67589), (67592, 67592), (67594, 67637), (67639, 67640), (67644, 67644), (67647, 67647)],
    'Cyrl': [(1024, 1156), (1159, 1327), (7296, 7306), (7467, 7467), (7544, 7544), (11744, 11775), (42560, 42655), (65070, 65071), (122928, 122989), (123023, 123023)],
    'Deva': [(2304, 2384), (2389, 2403), (2406, 2431), (43232, 43263), (72448, 72457)],
    'Diak': [(71936, 71942), (71945, 71945), (71948, 71955), (71957, 71958), (71960, 71989), (71991, 71992), (71995, 72006), (72016, 72025)],
    'Dogr': [(71680, 71739)],
    'Dsrt': [(66560, 66639)],
    'Dupl': [(113664, 113770), (113776, 113788), (113792, 113800), (113808, 113817), (113820, 113823)],
    'Egyp': [(77824, 78933), (78944, 82938)],
    'Elba': [(66816, 66855)],
    'Elym': [(69600, 69622)],
    'Ethi': [(4608, 4680), (4682, 4685), (4688, 4694), (4696, 4696), (4698, 4701), (4704, 4744), (4746, 4749), (4752, 4784), (4786, 4789), (4792, 4798), (4800, 4800), (4802, 4805), (4808, 4822), (4824, 4880), (4882, 4885), (4888, 4954), (4957, 4988), (4992, 5017), (11648, 11670), (11680, 11686), (11688, 11694), (11696, 11702), (11704, 11710), (11712, 11718), (11720, 11726), (11728, 11734), (11736, 11742), (43777, 43782), (43785, 43790), (43793, 43798), (43808, 43814), (43816, 43822), (124896, 124902), (124904, 124907), (124909, 124910), (124912, 124926)],
    'Gara': [(68928, 68965), (68969, 68997), (69006, 69007)],
    'Geor': [(4256, 4293), (4295, 4295), (4301, 4301), (4304, 4346), (4348, 4351), (7312, 7354), (7357, 7359), (11520, 11557), (11559, 11559), (11565, 11565)],
    'Glag': [(11264, 11359), (122880, 122886), (122888, 122904), (122907, 122913), (122915, 122916), (122918, 122922)],
    'Gong': [(73056, 73061), (73063, 73064), (73066, 73102), (73104, 73105), (73107, 73112), (73120, 73129)],
    'Gonm': [(72960, 72966), (72968, 72969), (72971, 73014), (73018, 73018), (73020, 73021), (73023, 73031), (73040, 73049)],
    'Goth': [(66352, 66378)],
    'Gran': [(70400, 70403), (70405, 70412), (70415, 70416), (70419, 70440), (70442, 70448), (70450, 70451), (70453, 70457), (70460, 70468), (70471, 70472), (70475, 70477), (70480, 70480), (70487, 70487), (70493, 70499), (70502, 70508), (70512, 70516)],
    'Grek': [(880, 883), (885, 887), (890, 893), (895, 895), (900, 900), (902, 902), (904, 906), (908, 908), (910, 929), (931, 993), (1008, 1023), (7462, 7466), (7517, 7521), (7526, 7530), (7615, 7615), (7936, 7957), (7960, 7965), (7968, 8005), (8008, 8013), (8016, 8023), (8025, 8025), (8027, 8027), (8029, 8029), (8031, 8061), (8064, 8116), (8118, 8132), (8134, 8147), (8150, 8155), (8157, 8175), (8178, 8180), (8182, 8190), (8486, 8486), (43877, 43877), (65856, 65934), (65952, 65952), (119296, 119365)],
    'Gujr': [(2689, 2691), (2693, 2701), (2703, 2705), (2707, 2728), (2730, 2736), (2738, 2739), (2741, 2745), (2748, 2757), (2759, 2761), (2763, 2765), (2768, 2768), (2784, 2787), (2790, 2801), (2809, 2815)],
    'Gukh': [(90368, 90425)],
    'Guru': [(2561, 2563), (2565, 2570), (2575, 2576), (2579, 2600), (2602, 2608), (2610, 2611), (2613, 2614), (2616, 2617), (2620, 2620), (2622, 2626), (2631, 2632), (2635, 2637), (2641, 2641), (2649, 2652), (2654, 2654), (2662, 2678)],
    'Hang': [(4352, 4607), (12334, 12335), (12593, 12686), (12800, 12830), (12896, 12926), (43360, 43388), (44032, 55203), (55216, 55238), (55243, 55291), (65440, 65470), (65474, 65479), (65482, 65487), (65490, 65495), (65498, 65500)],
    'Hani': [(11904, 11929), (11931, 12019), (12032, 12245), (12293, 12293), (12295, 12295), (12321, 12329), (12344, 12347), (13312, 19903), (19968, 40959), (63744, 64109), (64112, 64217), (94178, 94179), (94192, 94198), (131072, 173791), (173824, 178205), (178208, 183981), (183984, 191456), (191472, 192093), (194560, 195101), (196608, 201546), (201552, 210041)],
    'Hano': [(5920, 5940)],
    'Hatr': [(67808, 67826), (67828, 67829), (67835, 67839)],
    'Hebr': [(1425, 1479), (1488, 1514), (1519, 1524), (64285, 64310), (64312, 64316), (64318, 64318), (64320, 64321), (64323, 64324), (64326, 64335)],
    'Hira': [(12353, 12438), (12445, 12447), (110593, 110879), (110898, 110898), (110928, 110930), (127488, 127488)],
    'Hluw': [(82944, 83526)],
    'Hmng': [(92928, 92997), (93008, 93017), (93019, 93025), (93027, 93047), (93053, 93071)],
    'Hmnp': [(123136, 123180), (123184, 123197), (123200, 123209), (123214, 123215)],
    'Hung': [(68736, 68786), (68800, 68850), (68858, 68863)],
    'Ital': [(66304, 66339), (66349, 66351)],
    'Java': [(43392, 43469), (43472, 43481), (43486, 43487)],
    'Kali': [(43264, 43309), (43311, 43311)],
    'Kana': [(12449, 12538), (12541, 12543), (12784, 12799), (13008, 13054), (13056, 13143), (65382, 65391), (65393, 65437), (110576, 110579), (110581, 110587), (110589, 110590), (110592, 110592), (110880, 110882), (110933, 110933), (110948, 110951)],
    'Kawi': [(73472, 73488), (73490, 73530), (73534, 73562)],
    'Khar': [(68096, 68099), (68101, 68102), (68108, 68115), (68117, 68119), (68121, 68149), (68152, 68154), (68159, 68168), (68176, 68184)],
    'Khmr': [(6016, 6109), (6112, 6121), (6128, 6137), (6624, 6655)],
    'Khoj': [(70144, 70161), (70163, 70209)],
    'Kits': [(94180, 94180), (101120, 101589), (101631, 101631)],
    'Knda': [(3200, 3212), (3214, 3216), (3218, 3240), (3242, 3251), (3253, 3257), (3260, 3268), (3270, 3272), (3274, 3277), (3285, 3286), (3292, 3294), (3296, 3299), (3302, 3311), (3313, 3315)],
    'Krai': [(93504, 93561)],
    'Kthi': [(69760, 69826), (69837, 69837)],
    'Lana': [(6688, 6750), (6752, 6780), (6783, 6793), (6800, 6809), (6816, 6829)],
    'Laoo': [(3713, 3714), (3716, 3716), (3718, 3722), (3724, 3747), (3749, 3749), (3751, 3773), (3776, 3780), (3782, 3782), (3784, 3790), (3792, 3801), (3804, 3807)],
    'Latn': [(65, 90), (97, 122), (170, 170), (186, 186), (192, 214), (216, 246), (248, 696), (736, 740), (7424, 7461), (7468, 7516), (7522, 7525), (7531, 7543), (7545, 7614), (7680, 7935), (8305, 8305), (8319, 8319), (8336, 8348), (8490, 8491), (8498, 8498), (8526, 8526), (8544, 8584), (11360, 11391), (42786, 42887), (42891, 42972), (42993, 43007), (43824, 43866), (43868, 43876), (43878, 43881), (64256, 64262), (65313, 65338), (65345, 65370), (67456, 67461), (67463, 67504), (67506, 67514), (122624, 122654), (122661, 122666)],
    'Lepc': [(7168, 7223), (7227, 7241), (7245, 7247)],
    'Limb': [(6400, 6430), (6432, 6443), (6448, 6459), (6464, 6464), (6468, 6479)],
    'Lina': [(67072, 67382), (67392, 67413), (67424, 67431)],
    'Linb': [(65536, 65547), (65549, 65574), (65576, 65594), (65596, 65597), (65599, 65613), (65616, 65629), (65664, 65786)],
    'Lisu': [(42192, 42239), (73648, 73648)],
    'Lyci': [(66176, 66204)],
    'Lydi': [(67872, 67897), (67903, 67903)],
    'Mahj': [(69968, 70006)],
    'Maka': [(73440, 73464)],
    'Mand': [(2112, 2139), (2142, 2142)],
    'Mani': [(68288, 68326), (68331, 68342)],
    'Marc': [(72816, 72847), (72850, 72871), (72873, 72886)],
    'Medf': [(93760, 93850)],
    'Mend': [(124928, 125124), (125127, 125142)],
    'Merc': [(68000, 68023), (68028, 68047), (68050, 68095)],
    'Mero': [(67968, 67999)],
    'Mlym': [(3328, 3340), (3342, 3344), (3346, 3396), (3398, 3400), (3402, 3407), (3412, 3427), (3430, 3455)],
    'Modi': [(71168, 71236), (71248, 71257)],
    'Mong': [(6144, 6145), (6148, 6148), (6150, 6169), (6176, 6264), (6272, 6314), (71264, 71276)],
    'Mroo': [(92736, 92766), (92768, 92777), (92782, 92783)],
    'Mtei': [(43744, 43766), (43968, 44013), (44016, 44025)],
    'Mult': [(70272, 70278), (70280, 70280), (70282, 70285), (70287, 70301), (70303, 70313)],
    'Mymr': [(4096, 4255), (43488, 43518), (43616, 43647), (71376, 71395)],
    'Nagm': [(124112, 124153)],
    'Nand': [(72096, 72103), (72106, 72151), (72154, 72164)],
    'Narb': [(68224, 68255)],
    'Nbat': [(67712, 67742), (67751, 67759)],
    'Newa': [(70656, 70747), (70749, 70753)],
    'Nkoo': [(1984, 2042), (2045, 2047)],
    'Nshu': [(94177, 94177), (110960, 111355)],
    'Ogam': [(5760, 5788)],
    'Olck': [(7248, 7295)],
    'Onao': [(124368, 124410), (124415, 124415)],
    'Orkh': [(68608, 68680)],
    'Orya': [(2817, 2819), (2821, 2828), (2831, 2832), (2835, 2856), (2858, 2864), (2866, 2867), (2869, 2873), (2876, 2884), (2887, 2888), (2891, 2893), (2901, 2903), (2908, 2909), (2911, 2915), (2918, 2935)],
    'Osge': [(66736, 66771), (66776, 66811)],
    'Osma': [(66688, 66717), (66720, 66729)],
    'Ougr': [(69488, 69513)],
    'Palm': [(67680, 67711)],
    'Pauc': [(72384, 72440)],
    'Perm': [(66384, 66426)],
    'Phag': [(43072, 43127)],
    'Phli': [(68448, 68466), (68472, 68479)],
    'Phlp': [(68480, 68497), (68505, 68508), (68521, 68527)],
    'Phnx': [(67840, 67867), (67871, 67871)],
    'Plrd': [(93952, 94026), (94031, 94087), (94095, 94111)],
    'Prti': [(68416, 68437), (68440, 68447)],
    'Rjng': [(43312, 43347), (43359, 43359)],
    'Rohg': [(68864, 68903), (68912, 68921)],
    'Runr': [(5792, 5866), (5870, 5880)],
    'Samr': [(2048, 2093), (2096, 2110)],
    'Sarb': [(68192, 68223)],
    'Saur': [(43136, 43205), (43214, 43225)],
    'Sgnw': [(120832, 121483), (121499, 121503), (121505, 121519)],
    'Shaw': [(66640, 66687)],
    'Shrd': [(70016, 70111), (72544, 72551)],
    'Sidd': [(71040, 71093), (71096, 71133)],
    'Sidt': [(67904, 67929)],
    'Sind': [(70320, 70378), (70384, 70393)],
    'Sinh': [(3457, 3459), (3461, 3478), (3482, 3505), (3507, 3515), (3517, 3517), (3520, 3526), (3530, 3530), (3535, 3540), (3542, 3542), (3544, 3551), (3558, 3567), (3570, 3572), (70113, 70132)],
    'Sogd': [(69424, 69465)],
    'Sogo': [(69376, 69415)],
    'Sora': [(69840, 69864), (69872, 69881)],
    'Soyo': [(72272, 72354)],
    'Sund': [(7040, 7103), (7360, 7367)],
    'Sunu': [(72640, 72673), (72688, 72697)],
    'Sylo': [(43008, 43052)],
    'Syrc': [(1792, 1805), (1807, 1866), (1869, 1871), (2144, 2154)],
    'Tagb': [(5984, 5996), (5998, 6000), (6002, 6003)],
    'Takr': [(71296, 71353), (71360, 71369)],
    'Tale': [(6480, 6509), (6512, 6516)],
    'Talu': [(6528, 6571), (6576, 6601), (6608, 6618), (6622, 6623)],
    'Taml': [(2946, 2947), (2949, 2954), (2958, 2960), (2962, 2965), (2969, 2970), (2972, 2972), (2974, 2975), (2979, 2980), (2984, 2986), (2990, 3001), (3006, 3010), (3014, 3016), (3018, 3021), (3024, 3024), (3031, 3031), (3046, 3066), (73664, 73713), (73727, 73727)],
    'Tang': [(94176, 94176), (94208, 101119), (101632, 101662), (101760, 101874)],
    'Tavt': [(43648, 43714), (43739, 43743)],
    'Tayo': [(124608, 124638), (124640, 124661), (124670, 124671)],
    'Telu': [(3072, 3084), (3086, 3088), (3090, 3112), (3114, 3129), (3132, 3140), (3142, 3144), (3146, 3149), (3157, 3158), (3160, 3162), (3164, 3165), (3168, 3171), (3174, 3183), (3191, 3199)],
    'Tfng': [(11568, 11623), (11631, 11632), (11647, 11647)],
    'Tglg': [(5888, 5909), (5919, 5919)],
    'Thaa': [(1920, 1969)],
    'Thai': [(3585, 3642), (3648, 3675)],
    'Tibt': [(3840, 3911), (3913, 3948), (3953, 3991), (3993, 4028), (4030, 4044), (4046, 4052), (4057, 4058)],
    'Tirh': [(70784, 70855), (70864, 70873)],
    'Tnsa': [(92784, 92862), (92864, 92873)],
    'Todr': [(67008, 67059)],
    'Tols': [(73136, 73179), (73184, 73193)],
    'Toto': [(123536, 123566)],
    'Tutg': [(70528, 70537), (70539, 70539), (70542, 70542), (70544, 70581), (70583, 70592), (70594, 70594), (70597, 70597), (70599, 70602), (70604, 70613), (70615, 70616), (70625, 70626)],
    'Ugar': [(66432, 66461), (66463, 66463)],
    'Vaii': [(42240, 42539)],
    'Vith': [(66928, 66938), (66940, 66954), (66956, 66962), (66964, 66965), (66967, 66977), (66979, 66993), (66995, 67001), (67003, 67004)],
    'Wara': [(71840, 71922), (71935, 71935)],
    'Wcho': [(123584, 123641), (123647, 123647)],
    'Xpeo': [(66464, 66499), (66504, 66517)],
    'Xsux': [(73728, 74649), (74752, 74862), (74864, 74868), (74880, 75075)],
    'Yezi': [(69248, 69289), (69291, 69293), (69296, 69297)],
    'Yiii': [(40960, 42124), (42128, 42182)],
    'Zanb': [(72192, 72263)],
    'Zinh': [(768, 879), (1157, 1158), (2385, 2388), (6832, 6877), (6880, 6891), (7376, 7378), (7380, 7392), (7394, 7400), (7405, 7405), (7412, 7412), (7416, 7417), (7616, 7679), (8204, 8205), (8400, 8432), (12330, 12333), (12441, 12442), (65024, 65039), (65056, 65069), (66045, 66045), (66272, 66272), (70459, 70459), (118528, 118573), (118576, 118598), (119143, 119145), (119163, 119170), (119173, 119179), (119210, 119213), (917760, 917999)],
    'Zyyy': [(0, 64), (91, 96), (123, 169), (171, 185), (187, 191), (215, 215), (247, 247), (697, 735), (741, 745), (748, 767), (884, 884), (894, 894), (901, 901), (903, 903), (1541, 1541), (1548, 1548), (1563, 1563), (1567, 1567), (1600, 1600), (1757, 1757), (2274, 2274), (2404, 2405), (3647, 3647), (4053, 4056), (4347, 4347), (5867, 5869), (5941, 5942), (6146, 6147), (6149, 6149), (7379, 7379), (7393, 7393), (7401, 7404), (7406, 7411), (7413, 7415), (7418, 7418), (8192, 8203), (8206, 8292), (8294, 8304), (8308, 8318), (8320, 8334), (8352, 8385), (8448, 8485), (8487, 8489), (8492, 8497), (8499, 8525), (8527, 8543), (8585, 8587), (8592, 9257), (9280, 9290), (9312, 10239), (10496, 11123), (11126, 11263), (11776, 11869), (12272, 12292), (12294, 12294), (12296, 12320), (12336, 12343), (12348, 12351), (12443, 12444), (12448, 12448), (12539, 12540), (12688, 12703), (12736, 12773), (12783, 12783), (12832, 12895), (12927, 13007), (13055, 13055), (13144, 13311), (19904, 19967), (42752, 42785), (42888, 42890), (43056, 43065), (43310, 43310), (43471, 43471), (43867, 43867), (43882, 43883), (64830, 64831), (65040, 65049), (65072, 65106), (65108, 65126), (65128, 65131), (65279, 65279), (65281, 65312), (65339, 65344), (65371, 65381), (65392, 65392), (65438, 65439), (65504, 65510), (65512, 65518), (65529, 65532), (65792, 65794), (65799, 65843), (65847, 65855), (65936, 65948), (66000, 66044), (66273, 66299), (113824, 113827), (117760, 118012), (118016, 118451), (118458, 118480), (118496, 118512), (118608, 118723), (118784, 119029), (119040, 119078), (119081, 119142), (119146, 119162), (119171, 119172), (119180, 119209), (119214, 119274), (119488, 119507), (119520, 119539), (119552, 119638), (119648, 119672), (119808, 119892), (119894, 119964), (119966, 119967), (119970, 119970), (119973, 119974), (119977, 119980), (119982, 119993), (119995, 119995), (119997, 120003), (120005, 120069), (120071, 120074), (120077, 120084), (120086, 120092), (120094, 120121), (120123, 120126), (120128, 120132), (120134, 120134), (120138, 120144), (120146, 120485), (120488, 120779), (120782, 120831), (126065, 126132), (126209, 126269), (126976, 127019), (127024, 127123), (127136, 127150), (127153, 127167), (127169, 127183), (127185, 127221), (127232, 127405), (127462, 127487), (127489, 127490), (127504, 127547), (127552, 127560), (127568, 127569), (127584, 127589), (127744, 128728), (128732, 128748), (128752, 128764), (128768, 128985), (128992, 129003), (129008, 129008), (129024, 129035), (129040, 129095), (129104, 129113), (129120, 129159), (129168, 129197), (129200, 129211), (129216, 129217), (129232, 129240), (129280, 129623), (129632, 129645), (129648, 129660), (129664, 129674), (129678, 129734), (129736, 129736), (129741, 129756), (129759, 129770), (129775, 129784), (129792, 129938), (129940, 130042), (917505, 917505), (917536, 917631)],
    'Zzzz': [(65533, 65533)]
}



_CHAR_SCRIPTS: tp.Dict[int, tp.Tuple[str, ...]] = {}


def _char_scripts(ch: str) -> tp.Tuple[str, ...]:
    """The scripts (ISO 15924) of a character, from SCRIPT_RANGES; ('Zzzz',) for an uncoded character. A few
    characters belong to more than one script."""
    if not _CHAR_SCRIPTS:
        for key, ranges in SCRIPT_RANGES.items():
            for a, b in ranges:
                for o in range(a, b + 1):
                    _CHAR_SCRIPTS[o] = _CHAR_SCRIPTS.get(o, ()) + (key,)
    return _CHAR_SCRIPTS.get(ord(ch), ('Zzzz',))


ScoredScript = tp.Tuple[
    tp.Optional[str],
    float,
    tp.Dict[str, tp.Any]
]


def get_script_predictor(replace_punctuation=True, replace_digits=True) -> tp.Callable[[str], ScoredScript]:

    _char_scripts(' ')  # the shared character table (built once)

    replace_by = ""  # we just get rid of characters that are ubiquitous
    replacement_map = {
        ord(c): replace_by
        for c in string.whitespace
    }

    if replace_punctuation:
        replacement_map.update({ord(c): replace_by for c in string.punctuation})

    if replace_digits:
        replacement_map.update({ord(c): replace_by for c in string.digits})

    def predict_script(sent: str) -> ScoredScript:
        sent = sent.translate(replacement_map)

        char_counts = Counter(sent)
        script_count: tp.Dict[str, int] = defaultdict(int)

        for char, count in char_counts.items():
            ordinal = ord(char)
            for script_name in _CHAR_SCRIPTS.get(ordinal, ('Zzzz',)):
                script_count[script_name] += count


        # sort script_count alphabetically
        script_count = dict(sorted(script_count.items()))

        max_score = 0.0
        max_script = None
        for script, count in script_count.items():
            score = abs(count / len(sent))
            if score > max_score:
                max_score = score
                max_script = script


        # sort all the scores
        sorted_scores = {script: abs(count / len(sent)) for script, count in script_count.items()}
        sorted_scores = dict(sorted(sorted_scores.items(), key=lambda item: item[1], reverse=True))
        
        if len(sorted_scores) > 1:
            second_score = list(sorted_scores.values())[1]
            interval = max_score - second_score
            tie = True if interval == 0 else False
            return (max_script, max_score, {'details': sorted_scores, 'tie': tie, 'interval': interval})
        elif max_score == 0:
            return (None, 0, {'details': None, 'tie': None, 'interval': None})
        else:
            return (max_script, max_score, {'details': sorted_scores, 'tie': False, 'interval': 1})


    return predict_script



def separate_script(sent: str) -> Dict[str, str]:
    """
    Separates characters in the input string based on different scripts.

    Args:
        sent (str): Input string containing characters from different scripts.

    Returns:
        Dict[str, str]: A dictionary mapping script names to the separated characters. Every script gets every
        space of the input, so the words of a script keep their positions relative to each other.
    """
    _char_scripts(' ')
    marks = [(char, () if char == ' ' else _CHAR_SCRIPTS.get(ord(char), ())) for char in sent]
    seen = {script for _, scripts in marks for script in scripts}
    present = [script for script in SCRIPT_RANGES if script in seen]
    # every script present gets its characters and every space, in input order (characters outside every range
    # are dropped)
    result = {script: [char for char, scripts in marks if char == ' ' or script in scripts] for script in present}

    # Filter out empty values and spaces, and convert the list of characters to a string
    result = {key: ''.join(value) for key, value in result.items() if value and ''.join(value).strip()}

    return result


# ISO 15924 codes for writing systems that combine or vary Unicode scripts: which Unicode scripts each one uses.
COMPOSITE_SCRIPTS: Dict[str, tp.FrozenSet[str]] = {
    'Jpan': frozenset({'Hani', 'Hira', 'Kana'}),  # Japanese
    'Hrkt': frozenset({'Hira', 'Kana'}),          # Japanese syllabaries
    'Kore': frozenset({'Hang', 'Hani'}),          # Korean
    'Hanb': frozenset({'Hani', 'Bopo'}),          # Han with Bopomofo
    'Hans': frozenset({'Hani'}),                  # Simplified Han
    'Hant': frozenset({'Hani'}),                  # Traditional Han
}


def script_covers(writing_system: str, script: str) -> bool:
    """
    Whether a writing system (an ISO 15924 code, e.g. the script of a language label such as 'Jpan' in jpn_Jpan)
    is written with characters of a Unicode script (as returned by sp, ss or ws).

    Args:
        writing_system (str): ISO 15924 code of the writing system, a Unicode script or a composite code such as
            Jpan, Kore, Hans, Hant, Hanb or Hrkt.
        script (str): ISO 15924 code of a Unicode script.

    Returns:
        bool: True if the writing system uses that script.

    Example:
        >>> script_covers('Jpan', 'Hira'), script_covers('Kore', 'Hani'), script_covers('Latn', 'Cyrl')
        (True, True, False)
    """
    return script in COMPOSITE_SCRIPTS.get(writing_system, frozenset({writing_system}))


ScriptSegment = tp.Tuple[str, int, int, str]

_COMMON = ('Zyyy',)


def script_segments(text: str, common: str = "merge") -> List[ScriptSegment]:
    """
    Cuts a text into consecutive segments of one script each.

    Args:
        text (str): Input text.
        common (str): How to treat characters of the Common script (Zyyy: spaces, digits, punctuation, most
            symbols). "merge" (default): a run of them joins the segments around it when both have the same script;
            otherwise it becomes its own Zyyy segment. "separate": every run of them is its own Zyyy segment.
            Combining marks (Zinh) always take the script of the character before them. A character that belongs
            to several scripts takes the script of the character before it when that is one of them.

    Returns:
        List[Tuple[str, int, int, str]]: (script, start, end, segment text) with text[start:end] == segment text,
        covering the whole text in order.

    Example:
        >>> script_segments("Hello Salut سلام 你好")
        [('Latn', 0, 11, 'Hello Salut'), ('Zyyy', 11, 12, ' '), ('Arab', 12, 16, 'سلام'), ('Zyyy', 16, 17, ' '),
         ('Hani', 17, 19, '你好')]
    """
    if common not in ("merge", "separate"):
        raise ValueError('common must be "merge" or "separate"')
    labels: List[str] = []
    prev = None
    for ch in text:
        scripts = _char_scripts(ch)
        if scripts == ('Zinh',) and prev is not None:
            sc_ = prev
        elif prev is not None and prev in scripts:
            sc_ = prev
        else:
            sc_ = scripts[0]
        labels.append(sc_)
        if sc_ not in _COMMON:
            prev = sc_
    # runs of equal labels
    runs: List[List] = []
    for i, sc_ in enumerate(labels):
        if runs and runs[-1][0] == sc_:
            runs[-1][2] = i + 1
        else:
            runs.append([sc_, i, i + 1])
    if common == "merge":
        merged: List[List] = []
        k = 0
        while k < len(runs):
            sc_, a, b = runs[k]
            if (sc_ in _COMMON and merged and k + 1 < len(runs) and merged[-1][0] == runs[k + 1][0]):
                merged[-1][2] = runs[k + 1][2]
                k += 2
                continue
            if merged and merged[-1][0] == sc_:
                merged[-1][2] = b
            else:
                merged.append([sc_, a, b])
            k += 1
        runs = merged
    return [(sc_, a, b, text[a:b]) for sc_, a, b in runs]


def word_scripts(text: str) -> List[tp.Tuple[str, str]]:
    """
    The main script of each white-space-separated word.

    Args:
        text (str): Input text.

    Returns:
        List[Tuple[str, str]]: (word, script) for each word, in order. The script is the most frequent one among the
        word's characters that are not Common (Zyyy) or inherited (Zinh), ties going to the first in the word; a
        word made only of Common characters (digits, punctuation) gets Zyyy.

    Example:
        >>> word_scripts("I love 你好, ok!")
        [('I', 'Latn'), ('love', 'Latn'), ('你好,', 'Hani'), ('ok!', 'Latn')]
    """
    out = []
    for word in text.split():
        counts: tp.Dict[str, int] = {}
        prev = None
        for ch in word:
            sc_ = _char_scripts(ch)[0]
            if sc_ == 'Zinh':  # a combining mark counts for the script of the character before it
                sc_ = prev
            if sc_ is not None and sc_ != 'Zyyy':
                counts[sc_] = counts.get(sc_, 0) + 1
                prev = sc_
        out.append((word, max(counts, key=counts.get) if counts else 'Zyyy'))
    return out


def test_predict_script():
    predictor_fn = get_script_predictor()

    assert predictor_fn("this is a latin script.")[:2] == ("Latn", 1.0)
    assert predictor_fn("isso é escrita latina 1234")[:2] == ("Latn", 1.0)
    assert predictor_fn("এটি বাংলা লিপি")[:2] == ("Beng", 1.0)
    assert predictor_fn("นี่คืออักษรไทย")[:2] == ("Thai", 1.0)
    assert predictor_fn("자미로콰이 Jamiroquai는 영국의 애시드 재즈 밴드이다 자미로콰이는 년대 초반 런던에서 활발하게 일어난 애시드 재즈")[:2] == ("Hang", 0.8148148148148148)
    assert predictor_fn("이어지는기사  에서그점  에관해알려줄것  입니다")[:2] == ("Hang", 1.0)

    # empty
    assert predictor_fn(string.digits)[:2] == (None, 0)
    assert predictor_fn(string.whitespace)[:2] == (None, 0)
    assert predictor_fn("")[:2] == (None, 0)


def test_separate_script():

    sent = "Hello Salut سلام 你好 こんにちは שלום مرحبا"
    detected_scripts = separate_script(sent)

    ground_truth = {
        'Latn': 'Hello Salut     ',
        'Hebr': '     שלום ',
        'Arab': '  سلام    مرحبا',
        'Hani': '   你好   ',
        'Hira': '    こんにちは  '
    }

    for key in ground_truth.keys():
        assert key in detected_scripts, f"Error: '{key}' script not found in detected scripts."
        
        detected_tokens = [x.strip() for x in detected_scripts[key].split() if len(x.strip()) != 0]
        ground_truth_tokens = [x.strip() for x in ground_truth[key].split() if len(x.strip()) != 0]

        assert sorted(detected_tokens) == sorted(ground_truth_tokens), f"Error: Tokens for key '{key}' do not match."


def test_replacement_character():
    assert _char_scripts("�") == ('Zzzz',)
    assert get_script_predictor()("��")[:2] == ("Zzzz", 1.0)


def test_script_segments():
    text = "Hello Salut سلام 你好"
    segs = script_segments(text)
    assert segs == [('Latn', 0, 11, 'Hello Salut'), ('Zyyy', 11, 12, ' '), ('Arab', 12, 16, 'سلام'),
                    ('Zyyy', 16, 17, ' '), ('Hani', 17, 19, '你好')]
    assert "".join(s[3] for s in segs) == text and all(text[a:b] == t for _, a, b, t in segs)
    # common characters between segments of the same script join them; combining marks stay with their letter
    assert script_segments("नमस्ते दुनिया, hello") == [('Deva', 0, 13, 'नमस्ते दुनिया'), ('Zyyy', 13, 15, ', '),
                                                     ('Latn', 15, 20, 'hello')]
    assert script_segments("é a") == [('Latn', 0, 4, 'é a')]
    assert script_segments("I love 你好", common="separate") == [('Latn', 0, 1, 'I'), ('Zyyy', 1, 2, ' '),
                                                                 ('Latn', 2, 6, 'love'), ('Zyyy', 6, 7, ' '),
                                                                 ('Hani', 7, 9, '你好')]
    assert script_segments("") == [] and script_segments("2024!") == [('Zyyy', 0, 5, '2024!')]


def test_script_covers():
    assert script_covers('Jpan', 'Hira') and script_covers('Jpan', 'Hani') and script_covers('Kore', 'Hang')
    assert script_covers('Hant', 'Hani') and script_covers('Latn', 'Latn')
    assert not script_covers('Latn', 'Cyrl') and not script_covers('Hani', 'Hira')


def test_word_scripts():
    assert word_scripts("I love 你好, ok!") == [('I', 'Latn'), ('love', 'Latn'), ('你好,', 'Hani'), ('ok!', 'Latn')]
    assert word_scripts("Привет, world. 2024") == [('Привет,', 'Cyrl'), ('world.', 'Latn'), ('2024', 'Zyyy')]
    assert word_scripts("   ") == []


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
