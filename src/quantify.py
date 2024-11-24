import json
import csv

def count_types(json_file, csv_file, movie_name):
    try:
        # Load the JSON data from the file
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Count the occurrences of each category
        category_counts = {}
        if movie_name in data:
            for entry in data[movie_name]:
                category = entry.get("category", "Uncategorized")
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Save the distribution to a CSV file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Count"])
            for category, count in category_counts.items():
                writer.writerow([category, count])
        
        print(f"Category distribution saved to {csv_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Input JSON and output CSV file paths
movie_name = ""
input_file = "data/*.json"  # Replace with the actual file path
output_file = f"{input_file}_dist.csv"  # Replace with the desired output file path

# Count categories and save to CSV
count_types(input_file, output_file, movie_name)
