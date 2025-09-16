import json
import base64
import os

# Mapping Cherax components to BBFAS
CHERAX_TO_BBFAS_MAPPING = {
    # Components (Clothes) - Cherax key -> (BBFAS Drawable, BBFAS Texture)
    "Beard": ("pCI1", "pCT1"),         # Mask
    "Hair": ("pCI2", "pCT2"),          # Hair
    "Torso": ("pCI3", "pCT3"),         # Gloves (mapped from Torso)
    "Legs": ("pCI4", "pCT4"),          # Leg
    "Hands": ("pCI5", "pCT5"),         # Bag (mapped from Hands)
    "Feet": ("pCI6", "pCT6"),          # Shoe
    "Teeth": ("pCI7", "pCT7"),         # Misc (mapped from Teeth/Accessories)
    "Special": ("pCI8", "pCT8"),       # Top2 (undershirt)
    "Special 2": ("pCI9", "pCT9"),     # Armor
    "Decal": ("pCI10", "pCT10"),       # Decals
    "Tuxedo/Jacket Bib": ("pCI11", "pCT11"),  # Top

    # Props - Cherax key -> (BBFAS Drawable, BBFAS Texture)
    "Head": ("pPi0", "pPt0"),          # Hat (props)
    "Eyes": ("pPi1", "pPt1"),          # Glasses
    "Ears": ("pPi2", "pPt2"),          # Ears
    "Mouth": ("pPi3", "pPt3"),         # Ears (mapped from Mouth)
    "Left Hand": ("pPi4", "pPt4"),     # Ears (mapped from Left Hand)
    "Right Hand": ("pPi5", "pPt5"),    # Ears (mapped from Right Hand)
    "Left Wrist": ("pPi6", "pPt6"),    # Watches
    "Right Wrist": ("pPi7", "pPt7"),   # Bracelets
}

OUTPUT_DIR = "output\BBFAS"

def create_output_dir():
    """Create the output folder if it does not exist"""
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

def cherax_to_bbfas(json_data, gender):
    """Convert a real Cherax JSON to BBFAS code"""
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Build the decoded content
        lines = ["Item", "DI"]
        
        # Clothes Drawable (pCI0-pCI11)
        components = data.get("components", {})
        
        # Add default pCI0
        lines.extend(["pCI0", "-1"])
        
        # Process other components
        for cherax_key, (drawable_key, texture_key) in CHERAX_TO_BBFAS_MAPPING.items():
            if drawable_key.startswith("pCI") and cherax_key in components:
                comp_data = components[cherax_key]
                drawable_value = comp_data.get("drawable", -1)
                lines.extend([drawable_key, str(drawable_value)])
        
        lines.append("/DI")
        lines.append("DT")
        
        # Clothes Texture (pCT0-pCT11)
        lines.extend(["pCT0", "-1"])  # Default pCT0
        
        for cherax_key, (drawable_key, texture_key) in CHERAX_TO_BBFAS_MAPPING.items():
            if texture_key.startswith("pCT") and cherax_key in components:
                comp_data = components[cherax_key]
                texture_value = comp_data.get("texture", 0)
                lines.extend([texture_key, str(texture_value)])
        
        lines.append("/DT")
        lines.append("Pi")
        
        # Props Drawable (pPi0-pPi7)
        props = data.get("props", {})
        
        for cherax_key, (drawable_key, texture_key) in CHERAX_TO_BBFAS_MAPPING.items():
            if drawable_key.startswith("pPi") and cherax_key in props:
                prop_data = props[cherax_key]
                drawable_value = prop_data.get("drawable", -1)
                lines.extend([drawable_key, str(drawable_value)])
        
        lines.append("/Pi")
        lines.append("Pt")
        
        # Props Texture (pPt0-pPt7)
        for cherax_key, (drawable_key, texture_key) in CHERAX_TO_BBFAS_MAPPING.items():
            if texture_key.startswith("pPt") and cherax_key in props:
                prop_data = props[cherax_key]
                texture_value = prop_data.get("texture", -1)
                lines.extend([texture_key, str(texture_value)])
        
        lines.extend(["/Pt", "/Item"])
        
        # Encode in base64
        content = "\n".join(lines)
        encoded_code = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        
        return encoded_code
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return None

def convert_cherax_to_bbfas(input_file, gender, output_filename=None):
    """Main function to convert Cherax to BBFAS"""
    create_output_dir()
    
    # Load the JSON file
    json_data = load_json_file(input_file)
    if not json_data:
        return None
    
    # Convert to BBFAS
    result = cherax_to_bbfas(json_data, gender)
    if result:
        if not output_filename:
            output_path = get_unique_filename(f"bbfas_outfit_{gender.lower()}", "txt")
        else:
            output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"✅ CHERAX → BBFAS conversion successful! Generated code: {output_path}")
        print(f"📋 BBFAS Code ({gender}):")
        print(result)
        return output_path
    else:
        print("❌ CHERAX → BBFAS conversion failed")
        return None

if __name__ == "__main__":
    print("🔄 REAL CHERAX → BBFAS CONVERTER")
    print("=" * 40)
    
    file_path = input("Enter the path to the CHERAX JSON file: ").strip()
    
    if not file_path:
        print("❌ Empty path!")
    elif not os.path.exists(file_path):
        print("❌ File not found!")
    else:
        print("\nCharacter gender:")
        print("1. FEMALE")
        print("2. MALE")
        
        while True:
            try:
                gender_choice = int(input("\nYour choice (1 or 2): "))
                if gender_choice in [1, 2]:
                    break
                else:
                    print("❌ Please enter 1 or 2")
            except ValueError:
                print("❌ Please enter a valid number")
        
        gender = "FEMALE" if gender_choice == 1 else "MALE"
        convert_cherax_to_bbfas(file_path, gender)