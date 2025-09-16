import os
import sys

try:
    import importlib.util

    # Always build paths relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bbfas_json_path = os.path.join(base_dir, "modules", "BBFAS-JSON.py")
    json_cherax_path = os.path.join(base_dir, "modules", "JSON-CHERAX.py")
    cherax_bbfas_path = os.path.join(base_dir, "modules", "CHERAX-BBFAS.py")

    spec1 = importlib.util.spec_from_file_location("bbfas_json", bbfas_json_path)
    bbfas_json_module = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(bbfas_json_module)

    spec2 = importlib.util.spec_from_file_location("json_cherax", json_cherax_path)
    json_cherax_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(json_cherax_module)

    spec3 = importlib.util.spec_from_file_location("cherax_bbfas", cherax_bbfas_path)
    cherax_bbfas_module = importlib.util.module_from_spec(spec3)
    spec3.loader.exec_module(cherax_bbfas_module)

    convert_bbfas_to_json = getattr(bbfas_json_module, 'convert_bbfas_to_json')

    if hasattr(json_cherax_module, 'convert_json_to_cherax'):
        convert_json_to_cherax = getattr(json_cherax_module, 'convert_json_to_cherax')
    elif hasattr(cherax_bbfas_module, 'convert_json_to_cherax'):
        convert_json_to_cherax = getattr(cherax_bbfas_module, 'convert_json_to_cherax')
    else:
        raise AttributeError("convert_json_to_cherax not found in any module")

    if hasattr(cherax_bbfas_module, 'convert_cherax_to_bbfas'):
        convert_cherax_to_bbfas = getattr(cherax_bbfas_module, 'convert_cherax_to_bbfas')
    elif hasattr(json_cherax_module, 'convert_cherax_to_bbfas'):
        convert_cherax_to_bbfas = getattr(json_cherax_module, 'convert_cherax_to_bbfas')
    else:
        raise AttributeError("convert_cherax_to_bbfas not found in any module")

except (ImportError, FileNotFoundError, AttributeError) as e:
    print(f"❌ Import error : {e}")
    print("Make sure all files are in the correct structure:")
    print("📁 Required structure :")
    print("📁 src/")
    print("   main.py")
    print("   📁 modules/")
    print("      ├── BBFAS-JSON.py")
    print("      ├── JSON-CHERAX.py")
    print("      └── CHERAX-BBFAS.py")
    print(f"\n🔍 Current script file : {os.path.dirname(os.path.abspath(__file__))}")
    print(f"🔍 Looking for modules in : {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')}")
    sys.exit(1)

def display_menu():
    """Display the main menu"""
    print("🔄 Outfits converter - Main menu")
    print("=" * 50)
    print("1. 🔹 BBFAS CODE → JSON BBFAS")
    print("2. 🔸 JSON BBFAS → JSON CHERAX") 
    print("3. 🔹 JSON CHERAX → BBFAS CODE")
    print("4. 🚀 BBFAS CODE → JSON CHERAX (direct)")
    print("5. 🚀 JSON CHERAX → BBFAS CODE (direct)")
    # print("6. 🔄 COMPLETE CONVERSION (BBFAS → CHERAX → BBFAS)")
    print("0. ❌ Exit")

def get_user_choice():
    """Get the user's menu choice"""
    while True:
        try:
            choice = int(input("\n👉 Your choice (0-6): "))
            if 0 <= choice <= 6:
                return choice
            else:
                print("❌ Please enter a number between 0 and 6")
        except ValueError:
            print("❌ Please enter a valid number")

def get_gender():
    """Ask for the character's gender for BBFAS conversions"""
    print("\n👤 Character:")
    print("1. FEMALE")
    print("2. MALE")

    while True:
        try:
            gender_choice = int(input("\nYour choice (1 or 2): "))
            if gender_choice in [1, 2]:
                return "FEMALE" if gender_choice == 1 else "MALE"
            else:
                print("❌ Please enter 1 or 2")
        except ValueError:
            print("❌ Please enter a valid number")

def option_1():
    """BBFAS CODE → JSON BBFAS"""
    print("\n🔹 CONVERSION : BBFAS CODE → JSON BBFAS")
    print("-" * 40)

    code = input("Enter your BBFAS code : ").strip()
    if not code:
        print("❌ Empty code!")
        return

    result = convert_bbfas_to_json(code)
    if result:
        print(f"✅ Bbfas JSON file generated successfully!")

def option_2():
    """JSON BBFAS → JSON CHERAX"""
    print("\n🔸 CONVERSION : JSON BBFAS → JSON CHERAX")
    print("-" * 40)

    file_path = input("Enter the path to the JSON BBFAS file : ").strip()
    if not file_path:
        print("❌ Empty path!")
        return

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return

    gender = get_gender()
    result = convert_json_to_cherax(file_path, gender)
    if result:
        print(f"✅ JSON CHERAX file ({gender}) generated successfully!")

def option_3():
    """JSON CHERAX → BBFAS CODE"""
    print("\n🔹 CONVERSION : JSON CHERAX → BBFAS CODE")
    print("-" * 40)

    file_path = input("Enter the path to the JSON Cherax file : ").strip()
    if not file_path:
        print("❌ Empty path!")
        return

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return

    gender = get_gender()
    result = convert_cherax_to_bbfas(file_path, gender)
    if result:
        print(f"✅ BBFAS code generated successfully!")

def option_4():
    """BBFAS CODE → JSON CHERAX (direct)"""
    print("\n🚀 DIRECT CONVERSION : BBFAS CODE → JSON CHERAX")
    print("-" * 50)

    code = input("Enter your BBFAS code : ").strip()
    if not code:
        print("❌ Empty code!")
        return

    gender = get_gender()

    # Step 1: BBFAS → JSON
    print("🔄 Step 1/2 : Converting BBFAS → JSON...")
    temp_json = convert_bbfas_to_json(code, "temp_bbfas.json")
    if not temp_json:
        return

    # Step 2: JSON → CHERAX
    print("🔄 Step 2/2 : Converting JSON → CHERAX...")
    result = convert_json_to_cherax(temp_json, gender, f"cherax_direct_{gender.lower()}.json")
    if result:
        print(f"✅ Direct conversion BBFAS → CHERAX ({gender}) successful!")

    try:
        os.remove(temp_json)
    except:
        pass

def option_5():
    """JSON CHERAX → BBFAS CODE (direct)"""
    print("\n🚀 DIRECT CONVERSION : JSON CHERAX → BBFAS CODE")
    print("-" * 50)

    file_path = input("Enter the path to the JSON Cherax file : ").strip()
    if not file_path:
        print("❌ Empty path!")
        return

    if not os.path.exists(file_path):
        print("❌ File not found!")
        return

    gender = get_gender()
    result = convert_cherax_to_bbfas(file_path, gender, f"bbfas_direct_{gender.lower()}.txt")
    if result:
        print("✅ Direct conversion CHERAX → BBFAS successful!")

def option_6():
    """COMPLETE CONVERSION (BBFAS → CHERAX → BBFAS)"""
    print("\n🔄 Complete conversion : BBFAS → CHERAX → BBFAS")
    print("-" * 50)

    code = input("Enter your BBFAS code : ").strip()
    if not code:
        print("❌ Empty code!")
        return

    gender = get_gender()
    # Step 1: BBFAS → JSON
    print("🔄 Step 1/3 : Converting BBFAS → JSON...")
    temp_json = convert_bbfas_to_json(code, "temp_bbfas_complete.json")
    if not temp_json:
        return

    # Step 2: JSON → CHERAX
    print("🔄 Step 2/3 : Converting JSON → CHERAX...")
    temp_cherax = convert_json_to_cherax(temp_json, gender, "temp_cherax_complete.json")
    if not temp_cherax:
        return

    # Step 3: CHERAX → BBFAS
    print("🔄 Step 3/3: Converting CHERAX → BBFAS...")
    result = convert_cherax_to_bbfas(temp_cherax, gender, f"bbfas_complete_{gender.lower()}.txt")
    if result:
        print(f"✅ Complete conversion ({gender}) successful!")
        print("📁 Generated files :")
        print(f"   - JSON BBFAS : {temp_json}")
        print(f"   - JSON CHERAX : {temp_cherax}")
        print(f"   - BBFAS final : {result}")

    try:
        os.remove(temp_json)
        os.remove(temp_cherax)
    except:
        pass

def main():
    """Main function"""
    print("🎮 Welcome to the outfits converter!")
    print("📁 All generated files will be saved in the folder 'src/output/'")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 0:
            print("👋 Bye!")
            break
        elif choice == 1:
            option_1()
        elif choice == 2:
            option_2()
        elif choice == 3:
            option_3()
        elif choice == 4:
            option_4()
        elif choice == 5:
            option_5()
        elif choice == 6:
            option_6()

        input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 User requested stop")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\n⏸️  Press Enter to close...")
    finally:
        input("\n⏸️  Press Enter to close the program...")