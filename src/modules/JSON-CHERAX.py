import json
import os

# Mapping of BBFAS components to Cherax
BBFAS_TO_CHERAX_MAPPING = {
    # Components (Clothes)
    "pCI0": None,  # No direct equivalent
    "pCI1": "Beard",        # Mask
    "pCI2": "Hair",         # Hair
    "pCI3": "Torso",        # Gloves (mapped to Torso)
    "pCI4": "Legs",         # Leg
    "pCI5": "Hands",        # Bag (mapped to Hands)
    "pCI6": "Feet",         # Shoe
    "pCI7": "Teeth",        # Misc (mapped to Teeth/Accessories)
    "pCI8": "Special",      # Top2 (undershirt)
    "pCI9": "Special 2",    # Armor
    "pCI10": "Decal",       # Decals
    "pCI11": "Tuxedo/Jacket Bib",  # Top

    # Props
    "pPi0": "Head",         # Hat (props)
    "pPi1": "Eyes",         # Glasses
    "pPi2": "Ears",         # Ears
    "pPi3": "Mouth",        # Ears (mapped to Mouth)
    "pPi4": "Left Hand",    # Ears (mapped to Left Hand)
    "pPi5": "Right Hand",   # Ears (mapped to Right Hand)
    "pPi6": "Left Wrist",   # Watches
    "pPi7": "Right Wrist",  # Bracelets
}

OUTPUT_DIR = r"src\output\CHERAX"

def create_output_dir():
    """Create the output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_unique_filename(base_name, extension):
    """Generate a unique filename"""
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}.{extension}")
    if os.path.exists(output_path):
        i = 1
        while True:
            new_path = os.path.join(OUTPUT_DIR, f"{base_name}-{i}.{extension}")
            if not os.path.exists(new_path):
                output_path = new_path
                break
            i += 1
    return output_path

def load_json_file(file_path):
    """Load a JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

def json_to_cherax(json_data, gender="MALE"):
    """Convert BBFAS JSON to Cherax format"""
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        models = {
            "MALE": 1885233650,    # mp_m_freemode_01
            "FEMALE": 2627665880   # mp_f_freemode_01
        }

        cherax_outfit = {
            "format": "Cherax Entity",
            "type": 2,
            "model": models.get(gender, models["MALE"]),
            "baseFlags": 66871,
            "components": {},
            "props": {},
            "face_features": {
                "Nose Width": 0.0,
                "Nose Peak": 0.0,
                "Nose Length": 0.0,
                "Nose Bone Curveness": 0.0,
                "Nose Tip": 0.0,
                "Nose Bone Twist": 0.0,
                "Eyebrow Height": 0.0,
                "Eyebrow Indent": 0.0,
                "Cheek Bones": 0.0,
                "Cheek Sideways Bone Size": 0.0,
                "Cheek Bones Width": 0.0,
                "Eye Opening": 0.0,
                "Lip Thickness": 0.0,
                "Jaw Bone Width": 0.0,
                "Jaw Bone Shape": 0.0,
                "Chin Bone": 0.0,
                "Chin Bone Length": 0.0,
                "Chin Bone Shape": 0.0,
                "Chin Hole": 0.0,
                "Neck Thickness": 0.0
            },
            "primary_hair_tint": 255,
            "secondary_hair_tint": 255
        }

        clothes_drawable = data.get("Item", {}).get("Clothes", {}).get("Drawable", {})
        clothes_texture = data.get("Item", {}).get("Clothes", {}).get("Texture", {})

        # Map BBFAS clothes components to Cherax format
        for bbfas_key, cherax_key in BBFAS_TO_CHERAX_MAPPING.items():
            if cherax_key and bbfas_key.startswith("pCI"):
                drawable_value = clothes_drawable.get(bbfas_key, -1)
                texture_key = bbfas_key.replace("pCI", "pCT")
                texture_value = clothes_texture.get(texture_key, 0)

                if isinstance(drawable_value, dict):
                    drawable_value = drawable_value.get("ID", -1)
                if isinstance(texture_value, dict):
                    texture_value = texture_value.get("ID", 0)

                cherax_outfit["components"][cherax_key] = {
                    "drawable": drawable_value,
                    "texture": texture_value,
                    "palette": 0
                }

        props_drawable = data.get("Item", {}).get("Props", {}).get("Drawable", {})
        props_texture = data.get("Item", {}).get("Props", {}).get("Texture", {})

        # Map BBFAS props components to Cherax format
        for bbfas_key, cherax_key in BBFAS_TO_CHERAX_MAPPING.items():
            if cherax_key and bbfas_key.startswith("pPi"):
                drawable_value = props_drawable.get(bbfas_key, -1)
                texture_key = bbfas_key.replace("pPi", "pPt")
                texture_value = props_texture.get(texture_key, -1)

                if isinstance(drawable_value, dict):
                    drawable_value = drawable_value.get("ID", -1)
                if isinstance(texture_value, dict):
                    texture_value = texture_value.get("ID", -1)

                cherax_outfit["props"][cherax_key] = {
                    "drawable": drawable_value,
                    "texture": texture_value
                }

        # Add default components if missing
        default_components = {
            "Head": {"drawable": 0, "texture": 0, "palette": 0}
        }

        for comp_name, comp_data in default_components.items():
            if comp_name not in cherax_outfit["components"]:
                cherax_outfit["components"][comp_name] = comp_data

        # Add default props if missing
        default_props = {
            "Hip": {"drawable": -1, "texture": -1}
        }

        for prop_name, prop_data in default_props.items():
            if prop_name not in cherax_outfit["props"]:
                cherax_outfit["props"][prop_name] = prop_data

        return cherax_outfit

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return None

def convert_json_to_cherax(input_file, gender="MALE", output_filename=None):
    """Convert BBFAS JSON to Cherax format and save to file"""
    create_output_dir()

    json_data = load_json_file(input_file)
    if not json_data:
        return None

    # Convert to Cherax
    result = json_to_cherax(json_data, gender)
    if result:
        if not output_filename:
            output_path = get_unique_filename(f"cherax_outfit_{gender.lower()}", "json")
        else:
            output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON conversion → Cherax ({gender}) successful! Generated file: {output_path}")
        return output_path
    else:
        print("❌ Error during JSON → CHERAX conversion")
        return None

if __name__ == "__main__":
    print("🔄 JSON BBFAS converter → Cherax ")
    print("=" * 40)

    file_path = input("Enter the path to the JSON BBFAS file: ").strip()

    if not file_path:
        print("❌ Empty path!")
    elif not os.path.exists(file_path):
        print("❌ File not found!")
    else:
        print("\n👤 Code Character Gender:")
        print("1. MALE")
        print("2. FEMALE")

        while True:
            try:
                gender_choice = int(input("\nYour choice (1 or 2): "))
                if gender_choice in [1, 2]:
                    break
                else:
                    print("❌ Please enter 1 or 2")
            except ValueError:
                print("❌ Please enter a valid number")

        gender = "MALE" if gender_choice == 1 else "FEMALE"
        convert_json_to_cherax(file_path, gender)