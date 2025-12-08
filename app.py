import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image

# ===========================================================
# MUST BE FIRST STREAMLIT COMMAND
# ===========================================================
st.set_page_config(
    page_title="Strawberry Leaf Disease Detector",
    page_icon="🍓",
    layout="centered"
)

# ===========================================================
# DEVICE
# ===========================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ===========================================================
# CLASS NAMES
# ===========================================================
class_names = [
    'angular_leafspot',
    'anthracnose_fruit_rot',
    'blossom_blight',
    'gray_mold',
    'leaf_spot',
    'powdery_mildew_fruit',
    'powdery_mildew_leaf'
]

# ===========================================================
# TRANSFORMS
# ===========================================================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ===========================================================
# LOAD MODEL
# ===========================================================
@st.cache_resource
def load_model():
    model = models.resnet18()
    model.fc = nn.Linear(model.fc.in_features, len(class_names))
    model.load_state_dict(torch.load("strawberry_model.pth", map_location=device))
    model.to(device)
    model.eval()
    return model

model = load_model()

# ===========================================================
# PREDICT FUNCTION
# ===========================================================
def predict_leaf_disease_pil(img):
    img_tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1)[0]

    pred_idx = torch.argmax(probs).item()
    return class_names[pred_idx], probs[pred_idx].item(), probs.cpu().tolist()

# ===========================================================
# UI + CUSTOM CSS
# ===========================================================
st.markdown("""
    <style>
    .uploadedImage img {
        border-radius: 12px;
        max-width: 350px !important;    /* small image */
    }
    .block-container {
        max-width: 700px;               /* compact page */
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍓 Strawberry Leaf Disease Detection")
st.write("Upload a strawberry leaf image to get instant prediction.")

# ===========================================================
# FILE UPLOAD
# ===========================================================
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")

    st.markdown("### 📷 Preview")
    st.image(img, caption="Uploaded Leaf Image", width=350)

    st.markdown("---")

    if st.button("🔍 Predict Disease"):
        with st.spinner("Analyzing leaf..."):
            pred_class, confidence, probabilities = predict_leaf_disease_pil(img)

        st.success("Prediction Completed!")

        st.markdown(f"### 🧾 Result: **{pred_class}**")
        st.markdown(f"**Confidence:** `{confidence:.2f}`")

        prob_dict = {cls: p for cls, p in zip(class_names, probabilities)}

        st.markdown("### 📊 Probability Distribution")
        st.bar_chart(prob_dict)
else:
    st.info("Please upload an image to continue.")
