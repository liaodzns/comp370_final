from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import json
import numpy as np
import glob
import os
import time

# nlpt stop words list + custom words
STOP_WORDS = ['venom', 'last', 'dance', 'conclave', 'anora','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
"mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

def load_and_process_data(file_paths):
    # store all articles by category
    category_docs = defaultdict(list)
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # get the first movie name from the data
            movie_key = list(data.keys())[0]
            articles = data[movie_key]
            
            # add articles to category groups
            for article in articles:
                # combine title and description with a space between them
                text = f"{article.get('title', '')} {article.get('description', '')}"
                category = article.get('category', 'Uncategorized')
                category_docs[category].append(text)
                
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
    
    return category_docs

def calculate_tfidf_by_category(category_docs):
    # TF-IDF vectorizer from sci-kit learn with custom stop words
    vectorizer = TfidfVectorizer(
        stop_words=STOP_WORDS,  
        max_features=100, 
        min_df=2,  
        token_pattern=r'(?u)\b[A-Za-z]+\b'  # only match word characters, no numbers
    )
    
    results = {}
    
    for category, docs in category_docs.items():
        if len(docs) < 2:  # skip categories with too few documents
            print(f"Skipping category '{category}' - needs at least 2 documents, found {len(docs)}")
            continue
            
        tfidf_matrix = vectorizer.fit_transform(docs)
        feature_names = vectorizer.get_feature_names_out()
        
        # calculate average TF-IDF scores across all documents in this category
        avg_tfidf = np.mean(tfidf_matrix.toarray(), axis=0)
        
        # sorted list of (word, score) tuples
        word_scores = [(word, score) for word, score in zip(feature_names, avg_tfidf)]
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        # top 10 terms for each category
        results[category] = word_scores[:10]
    
    return results

def print_results(results):
    print("\nTop terms by category (with TF-IDF scores):")
    print("-" * 80)
    
    for category, terms in sorted(results.items()):  # categories alphabetical
        print(f"\n{category}:")
        for term, score in terms:
            print(f"  {term:<20} {score:.4f}")

def save_results_to_json(results, output_path):
    json_results = {}
    for category, terms in results.items():
        json_results[category] = [
            {"term": term, "score": round(float(score), 4)}  # round to 4 decimal places
            for term, score in terms
        ]
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, indent=4)
    
    print(f"\nResults saved to: {output_path}")

def main():
    # Define the data directory and pattern for JSON files
    data_dir = "data"
    pattern = "**/*_updated.json"
    
    # all matching JSON files
    file_paths = glob.glob(os.path.join(data_dir, pattern), recursive=True)
    
    if not file_paths:
        print(f"No files found matching pattern '{pattern}' in directory '{data_dir}'")
        return
    
    print(f"Processing {len(file_paths)} files:")
    for path in file_paths:
        print(f"- {path}")
    
    # process all files
    category_docs = load_and_process_data(file_paths)
    
    # print summary of documents per category
    print("\nDocuments per category:")
    for category, docs in sorted(category_docs.items()):
        print(f"- {category}: {len(docs)} documents")
    
    # calculate TF-IDF scores
    results = calculate_tfidf_by_category(category_docs)
    
    # print results
    print_results(results)
    
    # save results to JSON file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join("output", f"tfidf_results_{timestamp}.json")
    save_results_to_json(results, output_path)

if __name__ == "__main__":
    main()