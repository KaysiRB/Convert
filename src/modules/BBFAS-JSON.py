import base64
import json
import os

OUTPUT_DIR = r"src\output\BBFAS"

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

def bbfas_to_json(code):
    """Convert a BBFAS code to raw JSON"""
    try:
        decoded_data = base64.b64decode(code).decode("utf-8").strip()
    except Exception as e:
        print(f"❌ Error: Invalid BBFAS code (base64 decoding failed) - {e}")
        return None
    
    lines = decoded_data.split("\n")
    
    result = {
        "Code": code,
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
                    
                    result["Item"][current_section][current_type][key] = item_id
    
    return result

def convert_bbfas_to_json(code, output_filename=None):
    """Main function to convert BBFAS to JSON"""
    create_output_dir()
    
    result = bbfas_to_json(code)
    if result:
        if not output_filename:
            output_path = get_unique_filename("bbfas_outfit", "json")
        else:
            output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        
        print(f"✅ BBFAS → JSON conversion successful! File generated: {output_path}")
        return output_path
    else:
        print("❌ BBFAS → JSON conversion failed")
        return None

if __name__ == "__main__":
    print("🔄 BBFAS → JSON CONVERTER")
    print("=" * 40)
    
    code = input("Enter your BBFAS code: ").strip()
    
    if not code:
        print("❌ Empty code!")
    else:
        convert_bbfas_to_json(code)