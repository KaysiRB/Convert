import os
import sys
import importlib.util

def debug_module_detailed(file_path, module_name):
    """Detailed debug of a module"""
    try:
        print(f"\n{'='*50}")
        print(f"📁 MODULE: {file_path}")
        print(f"{'='*50}")
        
        if not os.path.exists(file_path):
            print("❌ File not found")
            return None, []
        
        print(f"✅ File exists ({os.path.getsize(file_path)} bytes)")
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print("✅ Module loaded successfully")
        
        # List ALL functions
        all_items = dir(module)
        functions = []
        variables = []
        
        for name in all_items:
            if not name.startswith('_'):
                item = getattr(module, name)
                if callable(item):
                    functions.append(name)
                    print(f"🔧 FUNCTION: {name}()")
                    
                    # Try to get the signature
                    try:
                        import inspect
                        sig = inspect.signature(item)
                        print(f"   └─ Signature: {name}{sig}")
                    except:
                        print(f"   └─ (Signature not available)")
                else:
                    variables.append(name)
                    print(f"📊 VARIABLE: {name} = {type(item).__name__}")
        
        print(f"\n📋 SUMMARY:")
        print(f"   🔧 Functions: {len(functions)}")
        print(f"   📊 Variables: {len(variables)}")
        
        expected_functions = {
            'BBFAS-JSON.py': ['convert_bbfas_to_json', 'bbfas_to_json'],
            'JSON-CHERAX.py': ['convert_json_to_cherax', 'json_to_cherax'],
            'CHERAX-BBFAS.py': ['convert_cherax_to_bbfas', 'cherax_to_bbfas']
        }
        
        filename = os.path.basename(file_path)
        if filename in expected_functions:
            print(f"\n🎯 Expected functions for {filename}:")
            for expected in expected_functions[filename]:
                if expected in functions:
                    print(f"   ✅ {expected} - Found")
                else:
                    print(f"   ❌ {expected} - Missing")
        
        return module, functions
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None, []

def main():
    print("🔍 ADVANCED MODULE DIAGNOSTIC")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    modules_info = [
        (os.path.join("Modules", "BBFAS-JSON.py"), "bbfas_json"),
        (os.path.join("Modules", "JSON-CHERAX.py"), "json_cherax"),
        (os.path.join("Modules", "CHERAX-BBFAS.py"), "cherax_bbfas")
    ]
    
    results = {}
    
    for file_path, module_name in modules_info:
        module, functions = debug_module_detailed(file_path, module_name)
        results[module_name] = (module, functions)
    
    # Final analysis
    print("\n" + "="*60)
    print("🎯 Final analysis")
    print("="*60)
    
    # Check for inversions
    json_cherax_funcs = results.get('json_cherax', (None, []))[1]
    cherax_bbfas_funcs = results.get('cherax_bbfas', (None, []))[1]
    
    print("\n🔍 Verification of inversions:")
    
    if 'convert_cherax_to_bbfas' in json_cherax_funcs:
        print("⚠️  JSON-CHERAX.py contains convert_cherax_to_bbfas (should be in CHERAX-BBFAS.py)")
    
    if 'convert_json_to_cherax' in cherax_bbfas_funcs:
        print("⚠️  CHERAX-BBFAS.py contains convert_json_to_cherax (should be in JSON-CHERAX.py)")

    print("\n💡 RECOMMENDED SOLUTION:")
    print("1. Swap the contents of JSON-CHERAX.py and CHERAX-BBFAS.py")
    print("2. Or use the tool. Corrected that automatically manages these inversions")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ General error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\n⏸️  Press Enter to close...")