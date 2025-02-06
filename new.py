import streamlit as st
import pandas as pd
import os

# Load the Excel file
def load_data():
    file_path = 'Projects.xlsx'  # Change to your file path
    df = pd.read_excel(file_path)
    return df

# Custom CSS for styling
def custom_css():
    st.markdown("""
    <style>
    .youtube-btn {
        display: inline-block;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        color: #fff;
        background-color: #FF0000;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
    }
    .youtube-btn:hover {
        background-color: #c70000;
        transform: scale(1.1);
    }
    .title {
        font-size: 36px;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
    }
    .product-container {
        padding: 10px;
        border-radius: 12px;
        background-color: blue;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
        text-align: center;
    }
    .price-tag {
        font-size: 18px;
        font-weight: bold;
        color: #FFD700;
        margin-top: 8px;
    }
    .footer {
        display: flex;
        justify-content: space-around;
        text-align: center;
        font-size: 16px;
        color: #fff;
        background-color: rgba(0, 0, 0, 0.7);  /* Transparent background */
        padding: 20px;
        border-radius: 15px;
        margin-top: 40px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .footer .footer-box {
        width: 45%;
        padding: 10px;
    }
    .footer .footer-heading {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# Display the YouTube button
def display_youtube_button():
    st.markdown("<div style='text-align: center; font-size: 24px; color: #4CAF50;'>Check out my YouTube Channel!</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <a href="https://www.youtube.com/@letsbuildit2427/shorts" target="_blank" class="youtube-btn">Visit My YouTube</a>
    </div>
    """, unsafe_allow_html=True)

def display_footer():
    st.markdown("""
    <div class='footer'>
        <div class="footer-box">
            <div class="footer-heading">Delivery Available:</div>
            Shiva Temple (KC), M-Block Gate, BEL Lab Parking
        </div>
        <div class="footer-box">
            <div class="footer-heading">Payment Method:</div>
            Payment: 30% Advance and 70% at Delivery
        </div>
        <div class="footer-box">
            <div class="footer-heading">Contact Us:</div>
            <a href="https://wa.me/919407166260?text=Need%20Project" target="_blank" style="color: green; text-decoration: none; font-weight: bold;">Click Here</a> to WhatsApp Us
        </div>

    </div>
    """, unsafe_allow_html=True)

# Display project details with filters
def display_projects(df):
    st.markdown("<div class='title'>Project Catalog</div>", unsafe_allow_html=True)
    st.markdown("""Browse through our projects to find the perfect fit for you. Each project is carefully designed to meet your needs.""")
    display_youtube_button()
    
    search_query = st.text_input("Search Projects", "", placeholder="Search by name, explanation, or price...")
    
    # Price filter dropdown
    price_filter = st.selectbox("Filter by Price:", ["All", "Below ₹2000", "Below ₹2500", "Below ₹3000", "Below ₹4000"])
    
    # Apply search and price filter
    if search_query:
        df = df[df['PROJECT NAME'].str.contains(search_query, case=False, na=False) | 
                df['EXPLANATION'].str.contains(search_query, case=False, na=False) | 
                df['Price'].astype(str).str.contains(search_query, case=False, na=False)]
    
    if price_filter == "Below ₹2000":
        df = df[df['Price'] <= 2000]
    elif price_filter == "Below ₹2500":
        df = df[df['Price'] <= 2500]
    elif price_filter == "Below ₹3000":
        df = df[df['Price'] <= 3000]
    elif price_filter == "Below ₹4000":
        df = df[df['Price'] <= 4000]

    categories = df['Category'].unique().tolist()
    selected_category = st.selectbox("Filter by Category", ["All"] + categories, index=0)

    if selected_category != "All":
        df = df[df['Category'] == selected_category]
    
    cols = st.columns(2)
    
    for index, row in df.iterrows():
        project_name = row['PROJECT NAME']
        explanation = row['EXPLANATION']
        price = row['Price']
        image_path = row['Images']
        
        col_index = index % 2
        with cols[col_index]:
            with st.container():
                st.markdown(f"<div class='product-container'>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 24px; color: white;'>{project_name}</div>", unsafe_allow_html=True)
                
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.write("No image available")
                
                with st.expander(f"Learn More about {project_name}"):
                    st.write(explanation)
                    st.markdown(f"<div class='price-tag'>Price: ₹{price}</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)


# Main function
def main():
    custom_css()
    df = load_data()
    display_projects(df)
    display_footer()

if __name__ == "__main__":
    main()