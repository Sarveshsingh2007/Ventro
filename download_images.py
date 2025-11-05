import os
import requests

# ==== 🔧 CONFIGURATION ====
API_KEY = "53093716-d5d430fc9b7a99928f82963aa"
base_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(base_dir, "static", "images", "products")
os.makedirs(save_dir, exist_ok=True)

# ==== 🛒 PRODUCT SEARCH TERMS ====
products = {
    "product1.jpg": "tshirt",
    "product2.jpg": "jeans",
    "product3.jpg": "hoodie",
    "product4.jpg": "formal shirt",
    "product5.jpg": "wristwatch",
    "product6.jpg": "sunglasses",
    "product7.jpg": "leather wallet",
    "product8.jpg": "headphones",
    "product9.jpg": "smartwatch",
    "product10.jpg": "bluetooth speaker",
    "product11.jpg": "powerbank",
    "product12.jpg": "cookware set",
    "product13.jpg": "electric kettle",
    "product14.jpg": "mixer grinder",
    "product15.jpg": "honey jar",
    "product16.jpg": "coffee beans",
    "product17.jpg": "green tea",
    "product18.jpg": "face wash",
    "product19.jpg": "moisturizer",
    "product20.jpg": "hair serum",
    "product21.jpg": "yoga mat",
    "product22.jpg": "dumbbells",
    "product23.jpg": "resistance bands",
    "product24.jpg": "lego set",
    "product25.jpg": "rc car",
    "product26.jpg": "puzzle game",
    "product27.jpg": "office chair",
    "product28.jpg": "coffee table",
    "product29.jpg": "bookshelf",
    "product30.jpg": "acoustic guitar",
    "product31.jpg": "keyboard piano",
    "product32.jpg": "book",
    "product33.jpg": "notebooks",
    "product34.jpg": "car vacuum cleaner",
    "product35.jpg": "car phone mount"
}

# ==== 🚀 DOWNLOAD IMAGES ====
for filename, keyword in products.items():
    query = keyword.replace(" ", "+")
    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo&per_page=3"
    
    try:
        response = requests.get(url)
        data = response.json()
        if "hits" in data and len(data["hits"]) > 0:
            image_url = data["hits"][0]["largeImageURL"]
            image_data = requests.get(image_url).content
            with open(os.path.join(save_dir, filename), "wb") as f:
                f.write(image_data)
            print(f"✅ Saved: {filename} ({keyword})")
        else:
            print(f"⚠️ No image found for: {keyword}")
    except Exception as e:
        print(f"❌ Error downloading {keyword}: {e}")

print(f"\n🎉 All images saved in: {save_dir}")
