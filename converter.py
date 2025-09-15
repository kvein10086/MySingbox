import json
import os
import sys
from collections import defaultdict

def convert_list_to_json(list_file_path):
    """
    Converts a .list file to a geosite-compatible .json file.
    """
    output_dir = 'rules'
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(list_file_path))[0]
    json_file_path = os.path.join(output_dir, f"{base_name}.json")

    rules_data = defaultdict(list)
    
    try:
        with open(list_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(',')
                if len(parts) < 2:
                    continue

                # Normalize rule type, e.g., DOMAIN-SUFFIX -> domain_suffix
                rule_type = parts[0].lower().replace('-', '_')
                value = parts[1]
                
                # Add more rule types here if needed in the future
                supported_types = ["domain", "domain_suffix", "ip_cidr", "domain_keyword"]
                if rule_type in supported_types:
                    rules_data[rule_type].append(value)

    except FileNotFoundError:
        print(f"Error: Input file not found at {list_file_path}")
        return
    except Exception as e:
        print(f"An error occurred while processing {list_file_path}: {e}")
        return

    if not rules_data:
        print(f"No valid rules found in {list_file_path}. Skipping JSON creation.")
        return

    output_data = {
        "version": 2,
        "rules": [dict(rules_data)]
    }

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully converted {list_file_path} to {json_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python converter.py <path_to_list_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    convert_list_to_json(input_file)