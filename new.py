import streamlit as st
import pandas as pd
import os
import json
# Load the Excel file
def load_data():
    file_path = 'data.xlsx'  # Ensure this file exists
    return pd.read_excel(file_path)

def load_whatsapp_links():
    json_path = 'data.json'  # Ensure this file exists
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        return {item["PROJECT NAME"]: item["whatsapp_link"] for item in data}
    st.warning("Warning: 'whatsapp_links.json' not found!")
    return {}

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
        background-color: rgba(0, 0, 0, 0.7);
        padding: 20px;
        border-radius: 15px;
        margin-top: 40px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .whatsapp-btn {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        color: white;
        background-color: #25D366;
        border-radius: 8px;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Display YouTube button
def display_youtube_button():
    st.markdown("<div style='text-align: center; font-size: 24px; color: #4CAF50;'>Check out my YouTube Channel!</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <a href="https://www.youtube.com/@letsbuildit2427/shorts" target="_blank" class="youtube-btn">Visit My YouTube</a>
    </div>
    """, unsafe_allow_html=True)

# Display project details with filters
def display_projects(df, whatsapp_links):
    st.markdown("<div class='title'>Project Catalog</div>", unsafe_allow_html=True)
    search_query = st.text_input("Search Projects", "", placeholder="Search by name, explanation, or price...")

    price_filter = st.selectbox("Filter by Price:", ["All", "Below ₹2000", "Below ₹2500", "Below ₹3000", "Below ₹4000"])
    if search_query:
        df = df[df['PROJECT NAME'].str.contains(search_query, case=False, na=False)]

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
        with cols[index % 2]:
            st.markdown(f"<div class='product-container'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; color: white;'>{row['PROJECT NAME']}</div>", unsafe_allow_html=True)

            if os.path.exists(row['Images']):
                st.image(row['Images'], use_container_width=True)
            else:
                st.write("No image available")

            with st.expander(f"Learn More about {row['PROJECT NAME']}"):
                st.write(row['EXPLANATION'])
                st.markdown(f"<div class='price-tag'>Price: ₹{row['Price']}</div>", unsafe_allow_html=True)

                if row['PROJECT NAME'] in whatsapp_links:
                    whatsapp_url = whatsapp_links[row['PROJECT NAME']]
                    st.markdown(f"<a href='{whatsapp_url}' target='_blank' class='whatsapp-btn'>📩 Chat on WhatsApp</a>", unsafe_allow_html=True)
                
                # Video Link Handling
                if 'video_link' in row and pd.notna(row['video_link']):
                    video_link = str(row['video_link']).strip()
                    st.write(f"🔗 Extracted Video Link: {video_link}")
                    if "youtube.com" in video_link or "youtu.be" in video_link:
                        st.video(video_link)
                    elif "drive.google.com" in video_link:
                        if "view" in video_link:
                            file_id = video_link.split("/")[-2]
                            embed_url = f"https://drive.google.com/file/d/{file_id}/preview"
                            st.markdown(f'<iframe src="{embed_url}" width="100%" height="300"></iframe>', unsafe_allow_html=True)
                        else:
                            st.markdown(f"[📂 Open Google Drive Video]({video_link})", unsafe_allow_html=True)
                    else:
                        st.markdown(f"[🎥 Open Video]({video_link})", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# Display the footer
def display_footer():
    st.markdown("""
    <div class='footer'>
        <div><strong>Delivery Available:</strong> Shiva Temple (KC), M-Block Gate, BEL Lab Parking</div>
        <div><strong>Payment Method:</strong> 30% Advance and 70% at Delivery</div>
        <div><strong>Contact Us:</strong> <a href="https://wa.me/919407166260?text=Need%20Project" target="_blank" style="color: green; text-decoration: none; font-weight: bold;">Click Here</a> to WhatsApp Us</div>
    </div>
    """, unsafe_allow_html=True)

# Main function
def main():
    custom_css()
    df = load_data()
    if df.empty:
        return
    whatsapp_links = load_whatsapp_links()
    display_projects(df, whatsapp_links)
    display_footer()

if __name__ == "__main__":
    main()
