import json

def add_category_to_json(file_path, output_path, category_placeholder="Uncategorized"):
    try:
        # Load the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Add the 'category' field to each entry
        if "Venom" in data:
            for entry in data["Venom"]:
                entry["category"] = category_placeholder
        
        # Save the updated data to a new file
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Updated JSON file saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# input and output file paths
# not using argparse for this - just press the RUN button
input_file = "venom_2024_10_31.json"  # Replace with the actual file path
output_file = "venom_2024_10_31_updated.json"  # Replace with the desired output file path

# Add the category field
add_category_to_json(input_file, output_file)
