import streamlit as st
import requests

# ---------- Static Data ----------
soil_data = {
    "Black Soil": {
        "nutrients": ["Calcium", "Magnesium", "Iron"],
        "best_crops": ["Cotton", "Sorghum", "Millets"]
    },
    "Red Soil": {
        "nutrients": ["Potassium", "Phosphorus"],
        "best_crops": ["Groundnut", "Pulses", "Tobacco"]
    },
    "Alluvial Soil": {
        "nutrients": ["Phosphorus", "Nitrogen", "Potash"],
        "best_crops": ["Wheat", "Rice", "Sugarcane"]
    }
}

crop_info = {
    "Cotton": {
        "pests": ["Bollworm", "Aphids"],
        "diseases": ["Leaf curl", "Wilt"],
        "fertilizers": ["NPK 20:20:0", "Calcium Nitrate"]
    },
    "Rice": {
        "pests": ["Stem borer", "Leaf folder"],
        "diseases": ["Blast", "Bacterial blight"],
        "fertilizers": ["Urea", "DAP", "Potash"]
    },
    "Groundnut": {
        "pests": ["Leaf miner", "White grub"],
        "diseases": ["Tikka leaf spot"],
        "fertilizers": ["Gypsum", "Zinc sulphate"]
    }
}

# ---------- Hugging Face Chat API ----------
HF_TOKEN = "hf_your_token_here"  # 🔁 Replace this with your real token
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-1B-distill"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def chat_with_bot(user_message):
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": user_message},
            timeout=15
        )
        result = response.json()
        if isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        elif isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif "error" in result:
            return "🤖 Error: Model loading or token issue"
        else:
            return "🤖 No response from AgriBot"
    except Exception as e:
        return f"❌ Exception: {str(e)}"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Smart Agri Info & Assistant", page_icon="🌿")

st.title("🌾 Smart Agri Info & Assistant")
st.markdown("Choose **soil or crop type** OR ask **AgriBot** below!")

tab1, tab2 = st.tabs(["🧪 Soil & Crop Info", "💬 AgriBot Chat"])

# --- Tab 1: Soil & Crop Info ---
with tab1:
    st.subheader("🪨 Soil Type Info")
    soil_type = st.selectbox("Select Soil Type", list(soil_data.keys()))
    if soil_type:
        st.markdown(f"**Nutrients in {soil_type}:** {', '.join(soil_data[soil_type]['nutrients'])}")
        st.markdown(f"**Best Crops:** {', '.join(soil_data[soil_type]['best_crops'])}")

    st.divider()

    st.subheader("🌱 Crop Info")
    crop = st.selectbox("Select Crop", list(crop_info.keys()))
    if crop:
        st.markdown(f"**Pests:** {', '.join(crop_info[crop]['pests'])}")
        st.markdown(f"**Diseases:** {', '.join(crop_info[crop]['diseases'])}")
        st.markdown(f"**Fertilizers:** {', '.join(crop_info[crop]['fertilizers'])}")

# --- Tab 2: Chatbot ---
with tab2:
    st.subheader("💬 Ask AgriBot")
    user_input = st.text_input("🧑‍🌾 You:", placeholder="e.g., Best crop for June in Telangana?")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if user_input:
        st.session_state.chat_history.append({"user": user_input})
        bot_reply = chat_with_bot(user_input)
        st.session_state.chat_history.append({"bot": bot_reply})

    for msg in st.session_state.chat_history:
        if "user" in msg:
            st.markdown(f"🧑‍🌾: {msg['user']}")
        if "bot" in msg:
            st.markdown(f"🤖: {msg['bot']}")
