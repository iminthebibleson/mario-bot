import json
import idaapi
import idautils
import idc

def export_bot_data():
    data = {
        "sprites": [],
        "profiles": [],
        "functions": [],
        "strings": []
    }

    # 1. Export all functions (name, address, demangled name)
    for ea in idautils.Functions():
        name = idc.get_func_name(ea)
        demangled = idc.demangle_name(name, idc.get_inf_attr(idc.INF_SHORT_DN))
        data["functions"].append({
            "address": hex(ea),
            "name": name,
            "demangled": demangled if demangled else name
        })

    # 2. Export sprites (you need to define what a "sprite" is in your DB)
    # Since you have a partially reversed IDB, you may have named data structures.
    # Example: if you have an array of sprite info at a known address:
    # sprite_array = idaapi.get_dword(0x60C9D0A0)  # adjust to your actual address
    # Then iterate and extract.

    # 3. Export profiles (similar to sprites)

    # 4. Export strings (useful for searching)
    for ea in idautils.Strings():
        data["strings"].append({
            "address": hex(ea.ea),
            "value": str(ea)
        })

    # Save to file
    output_path = idc.get_input_file_path() + "_bot_data.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Exported to: {output_path}")

if __name__ == "__main__":
    export_bot_data()