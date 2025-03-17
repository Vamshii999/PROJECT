from pymongo import MongoClient
from collections import Counter
import re

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['feed_ranking_db']
collection = db['reviews']

# Function to generate tags from summaries
def generate_tags(summary):
    words = re.findall(r'\b\w+\b', summary.lower())
    stopwords = set(['the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'with', 'on', 'this', 'that', 'was', 'as', 'are'])
    tags = [word for word in words if word not in stopwords and len(word) > 2]
    return tags

# Function to calculate top tags
def calculate_top_tags(tags_list):
    tag_frequency = Counter(tags_list)
    top_tags = tag_frequency.most_common(10)  # Top 10 tags
    return dict(top_tags)

# Update existing documents with tags and top_tags
def update_documents():
    # Fetch all unique product names
    product_names = collection.distinct('product_name')

    for product_name in product_names:
        # Fetch all reviews for the product
        product_reviews = list(collection.find({'product_name': product_name}))

        # Collect all summaries and tags for the product
        all_summaries = []
        all_tags = []

        for review in product_reviews:
            summary = review.get('Summary', '')
            # Ensure summary is a string
            if isinstance(summary, str):
                all_summaries.append(summary)
                tags = generate_tags(summary)
                all_tags.extend(tags)
                # Add tags to the review document
                collection.update_one(
                    {'_id': review['_id']},
                    {'$set': {'tags': tags}}
                )
            else:
                # Handle cases where summary is not a string (e.g., float, None)
                print(f"Skipping review with non-string summary: {review['_id']}")

        # Calculate top tags for the product
        top_tags = calculate_top_tags(all_tags)

        # Add top_tags to all reviews for the product
        collection.update_many(
            {'product_name': product_name},
            {'$set': {'top_tags': top_tags}}
        )

        print(f"Updated product: {product_name}")

if __name__ == "__main__":
    update_documents()