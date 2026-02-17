import os
import urllib.request

UCD_BASE = "https://www.unicode.org/Public/UCD/latest/ucd/"
FILE_NAME = "PropertyValueAliases.txt"
LOCAL_FILE = FILE_NAME


def download_file():
    if not os.path.isfile(LOCAL_FILE):
        print("Downloading PropertyValueAliases.txt...")
        urllib.request.urlretrieve(UCD_BASE + FILE_NAME, LOCAL_FILE)


def build_script_mapping():
    mapping = {}

    with open(LOCAL_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(";")]

            # Only Script property
            if parts[0] != "sc":
                continue

            # Format:
            # sc ; short-name ; long-name ; aliases...
            #
            # Example:
            # sc ; Xsux ; Cuneiform ; Sumero-Akkadian_Cuneiform

            if len(parts) >= 3:
                iso_code = parts[1]     # ISO 15924 code
                script_name = parts[2]  # Unicode long name

                mapping[script_name] = iso_code

    return mapping


if __name__ == "__main__":
    download_file()
    script_map = build_script_mapping()

    print("SCRIPT_NAME_TO_ISO = {")
    for name in sorted(script_map):
        print(f'    "{name}": "{script_map[name]}",')
    print("}")
