import zipfile
import sys
import json

def sb3_to_json(sb3_path, json_path=None):
    with zipfile.ZipFile(sb3_path, 'r') as z:
        with z.open('project.json') as f:
            project_data = json.load(f)
            if json_path:
                with open(json_path, 'w', encoding='utf-8') as out:
                    json.dump(project_data, out, indent=2)
            return project_data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sb3_to_json.py <input.sb3> [output.json]")
        sys.exit(1)
    sb3_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = sb3_to_json(sb3_file, json_file)
    print(json.dumps(result, indent=2))