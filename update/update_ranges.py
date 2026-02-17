import os
import urllib.request
from collections import defaultdict

UNICODE_URL = "https://www.unicode.org/Public/UCD/latest/ucd/Scripts.txt"
LOCAL_PATH = "Scripts.txt"


# Mapping Unicode script names → ISO 15924 codes
SCRIPT_NAME_TO_ISO = {
    "Adlam": "Adlm",
    "Ahom": "Ahom",
    "Anatolian_Hieroglyphs": "Hluw",
    "Arabic": "Arab",
    "Armenian": "Armn",
    "Avestan": "Avst",
    "Balinese": "Bali",
    "Bamum": "Bamu",
    "Bassa_Vah": "Bass",
    "Batak": "Batk",
    "Bengali": "Beng",
    "Beria_Erfe": "Berf",
    "Bhaiksuki": "Bhks",
    "Bopomofo": "Bopo",
    "Brahmi": "Brah",
    "Braille": "Brai",
    "Buginese": "Bugi",
    "Buhid": "Buhd",
    "Canadian_Aboriginal": "Cans",
    "Carian": "Cari",
    "Caucasian_Albanian": "Aghb",
    "Chakma": "Cakm",
    "Cham": "Cham",
    "Cherokee": "Cher",
    "Chorasmian": "Chrs",
    "Common": "Zyyy",
    "Coptic": "Copt",
    "Cuneiform": "Xsux",
    "Cypriot": "Cprt",
    "Cypro_Minoan": "Cpmn",
    "Cyrillic": "Cyrl",
    "Deseret": "Dsrt",
    "Devanagari": "Deva",
    "Dives_Akuru": "Diak",
    "Dogra": "Dogr",
    "Duployan": "Dupl",
    "Egyptian_Hieroglyphs": "Egyp",
    "Elbasan": "Elba",
    "Elymaic": "Elym",
    "Ethiopic": "Ethi",
    "Garay": "Gara",
    "Georgian": "Geor",
    "Glagolitic": "Glag",
    "Gothic": "Goth",
    "Grantha": "Gran",
    "Greek": "Grek",
    "Gujarati": "Gujr",
    "Gunjala_Gondi": "Gong",
    "Gurmukhi": "Guru",
    "Gurung_Khema": "Gukh",
    "Han": "Hani",
    "Hangul": "Hang",
    "Hanifi_Rohingya": "Rohg",
    "Hanunoo": "Hano",
    "Hatran": "Hatr",
    "Hebrew": "Hebr",
    "Hiragana": "Hira",
    "Imperial_Aramaic": "Armi",
    "Inherited": "Zinh",
    "Inscriptional_Pahlavi": "Phli",
    "Inscriptional_Parthian": "Prti",
    "Javanese": "Java",
    "Kaithi": "Kthi",
    "Kannada": "Knda",
    "Katakana": "Kana",
    "Katakana_Or_Hiragana": "Hrkt",
    "Kawi": "Kawi",
    "Kayah_Li": "Kali",
    "Kharoshthi": "Khar",
    "Khitan_Small_Script": "Kits",
    "Khmer": "Khmr",
    "Khojki": "Khoj",
    "Khudawadi": "Sind",
    "Kirat_Rai": "Krai",
    "Lao": "Laoo",
    "Latin": "Latn",
    "Lepcha": "Lepc",
    "Limbu": "Limb",
    "Linear_A": "Lina",
    "Linear_B": "Linb",
    "Lisu": "Lisu",
    "Lycian": "Lyci",
    "Lydian": "Lydi",
    "Mahajani": "Mahj",
    "Makasar": "Maka",
    "Malayalam": "Mlym",
    "Mandaic": "Mand",
    "Manichaean": "Mani",
    "Marchen": "Marc",
    "Masaram_Gondi": "Gonm",
    "Medefaidrin": "Medf",
    "Meetei_Mayek": "Mtei",
    "Mende_Kikakui": "Mend",
    "Meroitic_Cursive": "Merc",
    "Meroitic_Hieroglyphs": "Mero",
    "Miao": "Plrd",
    "Modi": "Modi",
    "Mongolian": "Mong",
    "Mro": "Mroo",
    "Multani": "Mult",
    "Myanmar": "Mymr",
    "Nabataean": "Nbat",
    "Nag_Mundari": "Nagm",
    "Nandinagari": "Nand",
    "New_Tai_Lue": "Talu",
    "Newa": "Newa",
    "Nko": "Nkoo",
    "Nushu": "Nshu",
    "Nyiakeng_Puachue_Hmong": "Hmnp",
    "Ogham": "Ogam",
    "Ol_Chiki": "Olck",
    "Ol_Onal": "Onao",
    "Old_Hungarian": "Hung",
    "Old_Italic": "Ital",
    "Old_North_Arabian": "Narb",
    "Old_Permic": "Perm",
    "Old_Persian": "Xpeo",
    "Old_Sogdian": "Sogo",
    "Old_South_Arabian": "Sarb",
    "Old_Turkic": "Orkh",
    "Old_Uyghur": "Ougr",
    "Oriya": "Orya",
    "Osage": "Osge",
    "Osmanya": "Osma",
    "Pahawh_Hmong": "Hmng",
    "Palmyrene": "Palm",
    "Pau_Cin_Hau": "Pauc",
    "Phags_Pa": "Phag",
    "Phoenician": "Phnx",
    "Psalter_Pahlavi": "Phlp",
    "Rejang": "Rjng",
    "Runic": "Runr",
    "Samaritan": "Samr",
    "Saurashtra": "Saur",
    "Sharada": "Shrd",
    "Shavian": "Shaw",
    "Siddham": "Sidd",
    "Sidetic": "Sidt",
    "SignWriting": "Sgnw",
    "Sinhala": "Sinh",
    "Sogdian": "Sogd",
    "Sora_Sompeng": "Sora",
    "Soyombo": "Soyo",
    "Sundanese": "Sund",
    "Sunuwar": "Sunu",
    "Syloti_Nagri": "Sylo",
    "Syriac": "Syrc",
    "Tagalog": "Tglg",
    "Tagbanwa": "Tagb",
    "Tai_Le": "Tale",
    "Tai_Tham": "Lana",
    "Tai_Viet": "Tavt",
    "Tai_Yo": "Tayo",
    "Takri": "Takr",
    "Tamil": "Taml",
    "Tangsa": "Tnsa",
    "Tangut": "Tang",
    "Telugu": "Telu",
    "Thaana": "Thaa",
    "Thai": "Thai",
    "Tibetan": "Tibt",
    "Tifinagh": "Tfng",
    "Tirhuta": "Tirh",
    "Todhri": "Todr",
    "Tolong_Siki": "Tols",
    "Toto": "Toto",
    "Tulu_Tigalari": "Tutg",
    "Ugaritic": "Ugar",
    "Unknown": "Zzzz",
    "Vai": "Vaii",
    "Vithkuqi": "Vith",
    "Wancho": "Wcho",
    "Warang_Citi": "Wara",
    "Yezidi": "Yezi",
    "Yi": "Yiii",
    "Zanabazar_Square": "Zanb",
}


def download_scripts():
    if not os.path.isfile(LOCAL_PATH):
        print("Downloading Scripts.txt...")
        urllib.request.urlretrieve(UNICODE_URL, LOCAL_PATH)


def parse_scripts():
    ranges = defaultdict(list)

    with open(LOCAL_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            left, right = line.split(";")
            script_name = right.strip().split()[0]

            if script_name not in SCRIPT_NAME_TO_ISO:
                continue  # skip scripts you don't map

            iso = SCRIPT_NAME_TO_ISO[script_name]

            code_range = left.strip().split("..")
            start = int(code_range[0], 16)
            end = int(code_range[-1], 16)

            ranges[iso].append((start, end))

    return ranges


def merge_ranges(ranges):
    merged = {}

    for script, intervals in ranges.items():
        intervals.sort()
        merged_list = []

        cur_start, cur_end = intervals[0]

        for start, end in intervals[1:]:
            if start <= cur_end + 1:
                cur_end = max(cur_end, end)
            else:
                merged_list.append((cur_start, cur_end))
                cur_start, cur_end = start, end

        merged_list.append((cur_start, cur_end))
        merged[script] = merged_list

    return merged


def print_dictionary(ranges):
    print("SCRIPT_RANGES = {")
    for script in sorted(ranges):
        print(f"    '{script}': {ranges[script]},")
    print("}")


if __name__ == "__main__":
    download_scripts()
    raw_ranges = parse_scripts()
    merged = merge_ranges(raw_ranges)
    print_dictionary(merged)
