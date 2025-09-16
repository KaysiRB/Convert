import base64
import json
import os

CODE = """SXRlbQpESQpwQ0kwCi0xCnBDSTEKMTAxCnBDSTIKLTEKcENJMwoxNTcKcENJNAoxODkKcENJNQowCnBDSTYKNzMKcENJNwoxMzkKcENJOAoyNDQKcENJOQowCnBDSTEwCjAKcENJMTEKMTk1Ci9ESQpEVApwQ1QwCi0xCnBDVDEKOQpwQ1QyCjAKcENUMwowCnBDVDQKMApwQ1Q1CjAKcENUNgoyMwpwQ1Q3CjAKcENUOAowCnBDVDkKMApwQ1QxMAowCnBDVDExCjQKL0RUClBpCnBQaTAKMTUKcFBpMQozNgpwUGkyCi0xCnBQaTMKLTEKcFBpNAotMQpwUGk1Ci0xCnBQaTYKMjEKcFBpNwoyCi9QaQpQdApwUHQwCjEKcFB0MQowCnBQdDIKLTEKcFB0MwotMQpwUHQ0Ci0xCnBQdDUKLTEKcFB0Ngo2CnBQdDcKMAovUHQKL0l0ZW0K"""

OUTPUT_DIR = "output\BBFAS"
BASE_FILENAME = "outfit.json"

# Dictionnaire des labels pour chaque type d'item
LABELS = {
    "Clothes": {
        "Drawable": {
            "pCI0": "",
            "pCI1": "Mask",
            "pCI2": "Hair", 
            "pCI3": "Gloves",
            "pCI4": "Leg",
            "pCI5": "Bag",
            "pCI6": "Shoe",
            "pCI7": "Misc",
            "pCI8": "Top2",
            "pCI9": "Armor",
            "pCI10": "Decals",
            "pCI11": "Top"
        },
        "Texture": {
            "pCT0": "",
            "pCT1": "Mask",
            "pCT2": "Hair",
            "pCT3": "Gloves", 
            "pCT4": "Leg",
            "pCT5": "Bag",
            "pCT6": "Shoe",
            "pCT7": "Misc",
            "pCT8": "Top2",
            "pCT9": "Armor",
            "pCT10": "Decals",
            "pCT11": "Top"
        }
    },
    "Props": {
        "Drawable": {
            "pPi0": "Hat",
            "pPi1": "Glasses",
            "pPi2": "Ears",
            "pPi3": "Ears",
            "pPi4": "Ears", 
            "pPi5": "Ears",
            "pPi6": "Watches",
            "pPi7": "Bracelets"
        },
        "Texture": {
            "pPt0": "Hat",
            "pPt1": "Glasses",
            "pPt2": "Ears",
            "pPt3": "Ears",
            "pPt4": "Ears",
            "pPt5": "Ears", 
            "pPt6": "Watches",
            "pPt7": "Bracelets"
        }
    }
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

output_path = os.path.join(OUTPUT_DIR, BASE_FILENAME)
if os.path.exists(output_path):
    i = 1
    while True:
        new_path = os.path.join(OUTPUT_DIR, f"outfit-{i}.json")
        if not os.path.exists(new_path):
            output_path = new_path
            break
        i += 1

decoded_data = base64.b64decode(CODE).decode("utf-8").strip()
lines = decoded_data.split("\n")

result = {
    "Code": CODE,
    "Item": {
        "Clothes": {"Drawable": {}, "Texture": {}},
        "Props": {"Drawable": {}, "Texture": {}}
    }
}

current_section = None
current_type = None

for line in lines:
    line = line.strip()
    if not line:
        continue

    if line == "DI":
        current_section = "Clothes"
        current_type = "Drawable"
        continue
    elif line == "DT":
        current_section = "Clothes"
        current_type = "Texture"
        continue
    elif line == "Pi":
        current_section = "Props"
        current_type = "Drawable"
        continue
    elif line == "Pt":
        current_section = "Props"
        current_type = "Texture"
        continue
    elif line.startswith("/"):
        current_section = None
        current_type = None
        continue

    if current_section and current_type:
        if line.startswith("p"):
            key = line
            value = next((v for v in lines[lines.index(line)+1:] if not v.startswith("p") and not v.isalpha() and not v.startswith("/")), None)
            if value is not None:
                try:
                    item_id = int(value)
                except ValueError:
                    item_id = value
                
                # Récupérer le label correspondant
                label = LABELS.get(current_section, {}).get(current_type, {}).get(key, "")
                
                # Créer l'objet avec ID et label
                result["Item"][current_section][current_type][key] = {
                    "ID": item_id,
                    "label": label
                }

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"✅ Fichier structuré généré avec labels : {output_path}")