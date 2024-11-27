import json
import matplotlib.pyplot as plt
from collections import defaultdict
import glob
import os

def plot_category_distribution_by_movie(json_files):
    try:
        # Initialize a dictionary to store category counts by movie
        movie_category_counts = defaultdict(lambda: defaultdict(int))

        # Process all JSON files
        for json_file in json_files:
            print(f"\nProcessing file: {json_file}")
            with open(json_file, 'r') as file:
                data = json.load(file)
                # Get movie title from filename and capitalize it
                movie_title = os.path.basename(json_file).split('_')[0].capitalize()
                print(f"Movie title: {movie_title}")
                print(f"Keys in data: {list(data.keys())}")
                
                # Populate the dictionary for this movie
                if movie_title in data:
                    print(f"Found {len(data[movie_title])} entries for {movie_title}")
                    for entry in data[movie_title]:
                        category = entry.get("category", "Uncategorized")
                        movie_category_counts[movie_title][category] += 1
                else:
                    print(f"Warning: Movie title '{movie_title}' not found in data")

        # Print the collected data
        print("\nCollected category counts:")
        for movie, categories in movie_category_counts.items():
            print(f"{movie}: {dict(categories)}")

        # Check if there are any movies to plot
        if not movie_category_counts:
            print("No movie data found to plot.")
            return

        # Plot the data
        fig, ax = plt.subplots(figsize=(12, 8))  # Increased figure size
        
        # Get all unique categories
        all_categories = set()
        for categories in movie_category_counts.values():
            all_categories.update(categories.keys())
        
        # Create bars for each movie
        x = range(len(all_categories))
        width = 0.8 / len(movie_category_counts)  # Adjust bar width based on number of movies
        
        for i, (movie, categories) in enumerate(movie_category_counts.items()):
            values = [categories.get(cat, 0) for cat in all_categories]
            ax.bar([xi + (i * width) for xi in x], 
                  values,
                  width,
                  label=movie,
                  alpha=0.7)

        # Customize the plot
        ax.set_title("Category Distribution Across All Movies")
        ax.set_xlabel("Category")
        ax.set_ylabel("Count")
        ax.set_xticks([xi + (width * len(movie_category_counts)/2) for xi in x])
        ax.set_xticklabels(list(all_categories), rotation=45, ha='right')
        ax.legend(title="Movies", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        # Save the diagram
        output_image = "data/diagrams/all_movies_distribution.png"
        plt.savefig(output_image, bbox_inches='tight')
        plt.show()
        print(f"Diagram saved to {output_image}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Get all JSON files
data_dir = "data"
pattern = "**/*_updated.json"
json_files = glob.glob(os.path.join(data_dir, pattern), recursive=True)

if not json_files:
    print(f"No files found matching pattern '{pattern}' in directory '{data_dir}'")
else:
    print(f"Processing {len(json_files)} files:")
    for path in json_files:
        print(f"- {path}")
    
    # Create the diagram
    plot_category_distribution_by_movie(json_files)
