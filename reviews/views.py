import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from collections import Counter
import re

client = MongoClient('mongodb://localhost:27017/')
db = client['feed_ranking_db']
collection = db['reviews']

def generate_tags(summary):
    words = re.findall(r'\b\w+\b', summary.lower())
    stopwords = set(['the', 'and', 'is', 'in', 'it', 'to', 'of', 'for', 'with', 'on', 'this', 'that', 'was', 'as', 'are'])
    tags = [word for word in words if word not in stopwords and len(word) > 2]
    return tags

def get_products(request):
    all_products = [review['product_name'] for review in collection.find()]
    return JsonResponse({'products': all_products})

def get_top_tags(request):
    all_tags = [tag for review in collection.find() for tag in review.get('tags', [])]
    tag_frequency = Counter(all_tags)
    top_tags = tag_frequency.most_common(10)
    return JsonResponse({'top_tags': dict(top_tags)})

def get_product_details(request, product_name):
    selected_product_reviews = list(collection.find({'product_name': product_name}))
    summaries = [review.get('Summary', '') for review in selected_product_reviews]
    tags = [tag for review in selected_product_reviews for tag in review.get('tags', [])]
    tag_frequency = Counter(tags)
    top_tags = tag_frequency.most_common(10)

    return JsonResponse({
        'product_name': product_name,
        'summaries': summaries,
        'tags': tags,
        'top_tags': dict(top_tags),
    })

@csrf_exempt
def search_summaries(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name')
            search_type = data.get('search_type')
            search_query = data.get('search_query')
            
            selected_product_reviews = collection.find({'product_name': product_name})
            search_results = []
            
            if search_type == 'tag':
                for review in selected_product_reviews:
                    if search_query in review.get('tags', []):
                        search_results.append(review['Summary'])
            
            elif search_type == 'keyword':
                for review in selected_product_reviews:
                    if search_query in review['Summary']:
                        search_results.append(review['Summary'])
            
            elif search_type == 'top_tag':
                tags = [tag for review in selected_product_reviews for tag in review.get('tags', [])]
                tag_frequency = Counter(tags)
                top_tags = dict(tag_frequency.most_common(10))
                
                if search_query in top_tags:
                    for review in selected_product_reviews:
                        if search_query in review.get('tags', []):
                            search_results.append(review['Summary'])

            return JsonResponse({
                'product_name': product_name,
                'search_type': search_type,
                'search_query': search_query,
                'results': search_results,
            })
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
