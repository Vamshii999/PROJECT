import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('amazon.csv')

# Display all unique brands
brands = df['brand'].unique()
print("Available Brands:")
for brand in brands:
    print(brand)

# Ask the user to select a brand
selected_brand = input("\nEnter the brand name to see its products: ")

# Filter the DataFrame for the selected brand
brand_products = df[df['brand'] == selected_brand]

# Display all product names under the selected brand
product_names = brand_products['product_name'].unique()
print(f"\nProducts under {selected_brand}:")
for product in product_names:
    print(product)

# Ask the user to select a product
selected_product = input("\nEnter the product name to see its reviews: ")

# Filter the DataFrame for the selected product
product_reviews = brand_products[brand_products['product_name'] == selected_product]

# Display all reviews of the selected product
print(f"\nReviews for {selected_product}:")
for index, row in product_reviews.iterrows():
    print(f"Review Header: {row['review_header']}")
    print(f"Review Text: {row['review_text']}")
    print("-" * 40)