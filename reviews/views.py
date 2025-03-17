from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from collections import Counter
import re

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['feed_ranking_db']  # Replace with your database name
collection = db['reviews']  # Replace with your collection name

# Function to generate tags from summaries
def generate_tags(summary):
    words = re.findall(r'\b\w+\b', summary.lower())
    stopwords = set(['the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'with', 'on', 'this', 'that', 'was', 'as', 'are'])
    tags = [word for word in words if word not in stopwords and len(word) > 2]
    return tags

# API to get all products (including duplicates)
def get_products(request):
    # Fetch all products (including duplicates)
    all_products = [review['product_name'] for review in collection.find()]
    return JsonResponse({'products': all_products})

# API to get top 10 tags across all products
def get_top_tags(request):
    all_tags = [tag for review in collection.find() for tag in review.get('tags', [])]
    tag_frequency = Counter(all_tags)
    top_tags = tag_frequency.most_common(10)
    return JsonResponse({'top_tags': dict(top_tags)})

# API to get details for a specific product (including duplicate summaries)
def get_product_details(request, product_name):
    # Fetch all reviews for the selected product
    selected_product_reviews = list(collection.find({'product_name': product_name}))
    
    # Get all summaries (including duplicates), handling missing 'summary' field
    summaries = [review.get('Summary', '') for review in selected_product_reviews]
    
    # Get all tags for the selected product, handling missing 'tags' field
    tags = [tag for review in selected_product_reviews for tag in review.get('tags', [])]
    tag_frequency = Counter(tags)
    top_tags = tag_frequency.most_common(10)  # Top 10 tags

    return JsonResponse({
        'product_name': product_name,
        'summaries': summaries,  # Includes duplicates
        'tags': tags,  # Includes duplicates
        'top_tags': dict(top_tags),  # Top 10 tags with frequency
    })
# API to search summaries by tag or keyword
@csrf_exempt
def search_summaries(request):
    if request.method == 'POST':
        product_name = request.body.get('product_name')
        search_type = request.body.get('search_type')
        search_query = request.body.get('search_query')
        
        # Fetch all reviews for the selected product
        selected_product_reviews = collection.find({'product_name': product_name})
        search_results = []
        
        if search_type == 'tag':
            # Search by tag
            for review in selected_product_reviews:
                if search_query in review.get('tags', []):
                    search_results.append(review['Summary'])
        
        elif search_type == 'keyword':
            # Search by keyword in the summary
            for review in selected_product_reviews:
                if search_query in review['Summary']:
                    search_results.append(review['Summary'])
        
        elif search_type == 'top_tag':
            # Search by top tags
            # Get the top tags for the product
            tags = [tag for review in selected_product_reviews for tag in review.get('tags', [])]
            tag_frequency = Counter(tags)
            top_tags = dict(tag_frequency.most_common(10))
            
            # Check if the search query is one of the top tags
            if search_query in top_tags:
                # If the search query is a top tag, gather summaries that contain this tag
                for review in selected_product_reviews:
                    if search_query in review.get('tags', []):
                        search_results.append(review['Summary'])

        return JsonResponse({
            'product_name': product_name,
            'search_type': search_type,
            'search_query': search_query,
            'results': search_results,
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
