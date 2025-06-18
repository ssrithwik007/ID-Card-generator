import streamlit as st
from generator import generate

st.set_page_config(page_title="ID Card Generator", layout="centered")

st.title("ID Card Generator")

with st.container():
    st.subheader("Sample template")
    st.image("assets/id_card_template_example.png", use_container_width=True)

# form_col, icon_col = st.columns(2, vertical_alignment="top", border = True)


with st.container():
    st.subheader("Fill the details below")

    title = st.text_input("Title of the ID Card", placeholder="e.g. Student ID Card")
    name = st.text_input("Name", placeholder="e.g. Smith")
    dob = st.text_input("Date of Birth", "01/01/2000")
    place = st.text_input("Place", placeholder="e.g. New York")
    ph_no = st.text_input("Phone Number", placeholder="e.g. +91 xxxxxxxxxx")
    spl_info = st.text_area("Special Information", placeholder="About the person", height=100, max_chars=250)
    photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"], label_visibility="collapsed")



st.subheader("Select an Icon")
with st.container():
    icon = st.slider(label="Select a watermark icon", min_value=1, max_value=16, value=1, step=1)
    col1, col2, col3 = st.columns(3)
    col2.image(f"assets/icons/icon_{icon}.png", width=150, use_container_width=True)

generate_button = st.button("Generate ID Card", use_container_width=True)


if generate_button:
    if not all([title, name, dob, place, ph_no, spl_info, photo]):
        st.error("Please fill all the fields and upload a photo.")
    else:
        id_card_image = generate({
            "title": title,
            "name": name,
            "dob": dob,
            "place": place,
            "ph_no": ph_no,
            "spl_info": spl_info,
            "photo": photo,
            "icon": icon
        })
        st.image(id_card_image, caption="Generated ID Card", use_container_width=True)
        st.download_button(
            label="Download ID Card",
            data=id_card_image,
            file_name=f"{name}_id_card.png",
            mime="image/png",
            use_container_width=True
        )
