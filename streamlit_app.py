import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO

# Define the API endpoints
BASE_URL = "http://44.201.129.4:8000"  # Adjust if your API is running elsewhere
HEADLINES_ENDPOINT = f"{BASE_URL}/get-headlines/"
TEMPLATE_ENDPOINT = f"{BASE_URL}/generate-template/"
SD_ENDPOINT = f"{BASE_URL}/generate-template-sd/"
SD_WITH_HEADLINES_ENDPOINT = f"{BASE_URL}/generate-template-sd-with-headlines/"

st.set_page_config(page_title="Product Ad Generator Tester", layout="wide")

st.title("Product Ad Generator Tester")

# Input form
with st.form("product_details_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Product Name", placeholder="e.g. Eco-Friendly Water Bottle")
        product_description = st.text_area("Product Description", placeholder="e.g. Stainless steel, double-walled insulated bottle")
    
    with col2:
        promo_details = st.text_input("Promotional Details (Optional)", placeholder="e.g. 25% off - Limited Time Offer")
        landing_page_url = st.text_input("Landing Page URL (Optional)", placeholder="https://example.com/products/water-bottle")
    
    # Endpoint selection
    endpoint_options = [
        "Generate Headlines Only",
        
        "Generate Template (Stability)",
        "Generate Template with Headlines (Stability)"
    ]
    endpoint_selection = st.selectbox("Select Endpoint to Test", endpoint_options)
    
    submit_button = st.form_submit_button("Generate")

# Process the form submission
if submit_button:
    # Prepare the request payload
    payload = {
        "name": product_name,
        "description": product_description
    }
    
    if promo_details:
        payload["promoDetails"] = promo_details
    
    if landing_page_url:
        payload["landingPageURL"] = landing_page_url
    
    with st.spinner("Processing request..."):
        try:
            # Call the selected endpoint
            if endpoint_selection == "Generate Headlines Only":
                response = requests.post(HEADLINES_ENDPOINT, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Headlines generated successfully!")
                    
                    # Display generated content
                    st.subheader("Generated Content")
                    st.markdown(f"**Product Name:** {data['name']}")
                    st.markdown(f"**Product Description:** {data['description']}")
                    
                    st.subheader("Generated Headlines")
                    for i, headline in enumerate(data['headlines'], 1):
                        st.markdown(f"**{i}.** {headline}")
                
            elif endpoint_selection == "Generate Template (DALL-E)":
                response = requests.post(TEMPLATE_ENDPOINT, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("DALL-E images generated successfully!")
                    
                    st.subheader("Generated Images")
                    columns = st.columns(len(data["image_urls"]))
                    
                    for i, (col, url) in enumerate(zip(columns, data["image_urls"])):
                        with col:
                            st.image(url, caption=f"Image {i+1}", use_column_width=True)
                            st.markdown(f"[Open in new tab]({url})")
            
            elif endpoint_selection == "Generate Template (Stability)":
                response = requests.post(SD_ENDPOINT, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Stability AI images generated successfully!")
                    
                    st.subheader("Generated Images")
                    columns = st.columns(len(data["image_urls"]))
                    
                    for i, (col, url) in enumerate(zip(columns, data["image_urls"])):
                        with col:
                            st.image(url, caption=f"Image {i+1}", use_column_width=True)
                            st.markdown(f"[Open in new tab]({url})")
            
            elif endpoint_selection == "Generate Template with Headlines (Stability)":
                response = requests.post(SD_WITH_HEADLINES_ENDPOINT, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Images with headlines generated successfully!")
                    
                    st.subheader("Generated Images")
                    columns = st.columns(len(data["image_urls"]))
                    
                    for i, (col, url) in enumerate(zip(columns, data["image_urls"])):
                        with col:
                            st.image(url, caption=f"Image {i+1}", use_column_width=True)
                            st.markdown(f"[Open in new tab]({url})")
            
            # Show response details in an expandable section
            with st.expander("View API Response Details"):
                st.json(response.json())
                
        except requests.exceptions.ConnectionError:
            st.error(f"Connection error: Make sure the API server is running at {BASE_URL}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if 'response' in locals() and hasattr(response, 'text'):
                st.error(f"API Response: {response.text}")

# Display API endpoints info
with st.expander("API Endpoints Information"):
    st.markdown("""
    ### Available Endpoints
    
    1. **GET /**: Health check endpoint
    2. **POST /get-headlines/**: Generates marketing headlines for a product
    4. **POST /generate-template-sd/**: Generates product ads using Stability AI
    5. **POST /generate-template-sd-with-headlines/**: Generates product ads with headlines using Stability AI
    
    ### Request Format Example
    ```json
    {
        "name": "Eco-Friendly Water Bottle",
        "description": "Stainless steel, double-walled insulated bottle",
        "promoDetails": "25% off - Limited Time Offer",
        "landingPageURL": "https://example.com/products/water-bottle"
    }
    ```
    """)

# Add instructions for running the app
st.sidebar.header("How to Use")
st.sidebar.markdown("""
1. Fill in the product details form
2. Select which endpoint you want to test
3. Click "Generate" to see the results

""")

# Add validation info
st.sidebar.header("Input Requirements")
st.sidebar.markdown("""
- **Product Name OR Description**: At least one must be provided
""")
