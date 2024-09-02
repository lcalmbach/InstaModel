
max_img = 50

IMAGE_PATH = Path('./data')

def search_images(term, max_images=max_img):
    print(f"Searching for '{term}'")
    with DDGS() as ddgs:
        search_results = ddgs.images(keywords=term)
        image_data = list(search_results)
        image_urls = [item.get("image") for item in image_data[:max_images]]
        return L(image_urls)


def empty_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def download_images(keyword, folder_path, max_images=10):
    images = []
    urls = search_images(keyword, max_images)
    os.makedirs(folder_path, exist_ok=True)
    empty_folder(folder_path)
    for i, url in enumerate(urls):
        image_filename = f"{keyword}_{i + 1}.jpg"
        image_path = os.path.join(folder_path, image_filename)
        try:
            img_data = requests.get(url).content
            img = Image.open(io.BytesIO(img_data))
            img.verify()
            with open(image_path, "wb") as f:
                f.write(img_data)
            images.append(image_path)
        except Exception as e:
            print(f"Error downloading {image_filename}: {e}")
    
    return images


def image_preview(image_dict):
    st.subheader("Image Preview")
    columns = st.sidebar.slider("Number of columns for preview", min_value=1, max_value=5, value=3)

    for keyword, images in image_dict.items():
        st.write(f"Category: {keyword}")
        cols = st.columns(columns)
        for i, img in enumerate(images):
            cols[i % columns].image(img, caption=f"{keyword} {i+1}", use_column_width=True)


def create_zip(image_dict, base_folder):
    """
    Creates a zip archive containing all images organized by category.
    
    Parameters:
    - image_dict (dict): Dictionary mapping keywords to lists of PIL.Image objects.
    - base_folder (str): Base directory where images are stored.
    
    Returns:
    - BytesIO: In-memory buffer containing the zip archive.
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for keyword, images in image_dict.items():
            folder_name = keyword.replace(" ", "_").lower()
            folder_path = os.path.join(base_folder, folder_name)
            for i, img in enumerate(images, start=1):
                img_filename = f"{folder_name}_{i}.jpg"
                img_path = os.path.join(folder_path, img_filename)
                if os.path.exists(img_path):
                    zip_file.write(img_path, arcname=os.path.join(folder_name, img_filename))
    zip_buffer.seek(0)
    return zip_buffer




keywords_input = st.sidebar.text_input("Keywords (comma-separated)", value="Basel,Berlin,Bern")

    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    if len(st.session_state.keywords) + len(keywords) <= 10:
        st.session_state.keywords = keywords
    else:
        st.warning("You can add up to 10 keywords only.")

    # Option to resize images
    resize = st.sidebar.checkbox("Resize images", value=True)

    if resize:
        cols = st.columns(2)
        with cols[0]:
            width = st.sidebar.number_input("Width", min_value=1, max_value=220, value=220)
        with cols[1]:
            height = st.sidebar.number_input("Height", min_value=1, max_value=220, value=220)
        max_num_images = 100
        def_num_images = 10
    else:
        max_num_images = 10
        def_num_images = 5

    num_images = st.sidebar.number_input("Number of images per keyword", min_value=1, max_value=max_num_images, value=def_num_images)

    if len(st.session_state.keywords) > 0:
        if st.sidebar.button("Download Images"):
            st.session_state.image_dict = {}
            if not st.session_state.keywords:
                st.warning("Please add at least one keyword.")
            else:
                for keyword in st.session_state.keywords:
                    folder_path = IMAGE_PATH / keyword.replace(" ", "_").lower()
                    with st.spinner(f"Downloading images for: {keyword}"):
                        st.session_state.image_dict[keyword] = download_images(keyword, folder_path, num_images)
                st.toast("Download complete!", icon='✅')
    if st.sidebar.button("make model"):
        st.session_state.model = Model(IMAGE_PATH, 'cities')
        st.session_state.model.train_model()

    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Predict"):
            st.session_state.model.model_predict(image_file)
            st.write(f"Prediction: {st.session_state.model.pred} (probability: {st.session_state.model.probs[st.session_state.model.pred_idx]:.4f})")    
