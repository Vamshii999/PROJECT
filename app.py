import pandas as pd
from collections import Counter
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key='AIzaSyCmWL4tQdxPqUV0iXlNBSZN4NJuyGy-3Xo')  # Replace with your Gemini API key
model = genai.GenerativeModel('gemini-1.5-flash')
# Load the CSV file into a DataFrame
df = pd.read_csv('reviews.csv')

# Handle NaN values in the 'Summary' column by filling them with empty strings
df['Summary'] = df['Summary'].fillna('')

# Function to generate tags using Gemini API
def generate_tags_with_gemini(summary):
    if not summary.strip():  # Skip empty summaries
        return []
    try:
        # Prompt Gemini to generate tags
        response = model.generate_content(f"Generate relevant tags for the following text: {summary}")
        time.sleep(1)
        tags = response.text.strip().split(',')  # Assuming tags are comma-separated
        tags = [tag.strip().lower() for tag in tags if tag.strip()]
        return tags
    except Exception as e:
        print(f"Error generating tags: {e}")
        return []

# Generate tags for all summaries
df['tags'] = df['Summary'].apply(generate_tags_with_gemini)

# Flatten the list of tags and count their frequency
all_tags = [tag for sublist in df['tags'] for tag in sublist]
tag_frequency = Counter(all_tags)

# Display the top 10 most frequent tags
top_tags = tag_frequency.most_common(10)
print("Top 10 Tags:")
for tag, count in top_tags:
    print(f"{tag}: {count}")

# Display all unique products
unique_products = df['product_name'].unique()
print("\nAvailable Products:")
for i, product in enumerate(unique_products, 1):
    print(f"{i}. {product}")

# Prompt the user to select a product
selected_index = int(input("\nSelect a product by number: ")) - 1
selected_product = unique_products[selected_index]

# Filter the DataFrame for the selected product
selected_product_df = df[df['product_name'] == selected_product]

# Display all summaries for the selected product
print(f"\nSummaries for '{selected_product}':")
for summary in selected_product_df['Summary']:
    print(f"- {summary}")

# Extract tags for the selected product
selected_product_tags = [tag for sublist in selected_product_df['tags'] for tag in sublist]
selected_product_tag_frequency = Counter(selected_product_tags)

# Display the top tags for the selected product
print("\nTop Tags for the Selected Product:")
top_selected_tags = selected_product_tag_frequency.most_common(10)
for tag, count in top_selected_tags:
    print(f"{tag}: {count}")

# Function to search summaries by keyword under the selected product
def search_summaries_by_keyword(keyword, product_df):
    results = []
    for index, row in product_df.iterrows():
        if keyword.lower() in row['Summary'].lower():
            results.append(row['Summary'])
    return results

# Function to search summaries by tag under the selected product
def search_summaries_by_tag(tag, product_df):
    results = []
    for index, row in product_df.iterrows():
        if tag in row['tags']:
            results.append(row['Summary'])
    return results

# Main interaction loop for searching
while True:
    print("\n1. Search by Keyword")
    print("2. Search by Tag")
    print("3. Exit")
    choice = input("Choose an option (1/2/3): ")

    if choice == '1':
        # Search by keyword
        keyword_to_search = input("Enter a keyword to search: ").lower()
        search_results = search_summaries_by_keyword(keyword_to_search, selected_product_df)
        if search_results:
            print(f"\nSummaries for '{selected_product}' containing the keyword '{keyword_to_search}':")
            for summary in search_results:
                print(f"- {summary}")
        else:
            print(f"No summaries found with the keyword '{keyword_to_search}'.")

    elif choice == '2':
        # Search by tag
        tag_to_search = input("Enter a tag to search: ").lower()
        search_results = search_summaries_by_tag(tag_to_search, selected_product_df)
        if search_results:
            print(f"\nSummaries for '{selected_product}' containing the tag '{tag_to_search}':")
            for summary in search_results:
                print(f"- {summary}")
        else:
            print(f"No summaries found with the tag '{tag_to_search}'.")

    elif choice == '3':
        # Exit the program
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")