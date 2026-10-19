import random
import streamlit as st

st.set_page_config(
    page_title="Nuôi Mèo Meo Meo 🐾",
    page_icon="🐱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS cho giao diện siêu cute
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF8E7;
    }
    .status-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 2px solid #FFE0B2;
        text-align: center;
        margin-bottom: 20px;
    }
    .cat-avatar {
        font-size: 90px;
        margin: 10px 0;
    }
    .stButton > button {
        border-radius: 15px;
        font-size: 18px;
        font-weight: bold;
        padding: 12px;
        background-color: #FFE0B2;
        color: #5D4037;
        border: 2px solid #FFB74D;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #FFB74D;
        color: white;
        transform: scale(1.03);
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Khởi tạo trạng thái nuôi mèo trong session_state
if "cat_name" not in st.session_state:
    st.session_state.cat_name = "Miu Miu"
if "hunger" not in st.session_state:
    st.session_state.hunger = 70  # Độ no (0 - 100)
if "happiness" not in st.session_state:
    st.session_state.happiness = 80  # Độ vui (0 - 100)
if "energy" not in st.session_state:
    st.session_state.energy = 60  # Năng lượng (0 - 100)
if "level" not in st.session_state:
    st.session_state.level = 1
if "exp" not in st.session_state:
    st.session_state.exp = 0
if "coins" not in st.session_state:
    st.session_state.coins = 50


def gain_exp(amount):
    st.session_state.exp += amount
    if st.session_state.exp >= 100:
        st.session_state.level += 1
        st.session_state.exp -= 100
        st.toast(
            f"🎉 {st.session_state.cat_name} đã lên Cấp {st.session_state.level}!",
            icon="⭐",
        )


# Xác định trạng thái & cảm xúc của Mèo
def get_cat_state():
    h = st.session_state.hunger
    happy = st.session_state.happiness
    e = st.session_state.energy

    if e <= 20:
        return "😴", "Buồn ngủ lắm rồi..."
    elif h <= 30:
        return "😾", "Đói bụng quá meoww!"
    elif happy <= 30:
        return "😿", "Đang chán đời nè..."
    elif happy >= 80 and h >= 70:
        return "😻", "Đang cực kỳ hạnh phúc!"
    else:
        return "🐱", "Ngoan ngoãn chờ bạn chơi cùng!"


cat_icon, cat_status_text = get_cat_state()

# ---------------- TIÊU ĐỀ & CẤP ĐỘ ----------------
st.title("🐾 Tiệm Nuôi Mèo Meo Meo 🐾")

col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Cấp độ", f"Lv.{st.session_state.level}")
col_info2.metric("Kinh nghiệm", f"{st.session_state.exp}/100 XP")
col_info3.metric("Túi xu", f"{st.session_state.coins} 💰")

# ---------------- HIỂN THỊ CHÚ MÈO ----------------
st.markdown(
    f"""
    <div class="status-card">
        <h2>{st.session_state.cat_name}</h2>
        <div class="cat-avatar">{cat_icon}</div>
        <p style="font-size: 18px; color: #8D4B38; font-weight: bold;">"{cat_status_text}"</p>
    </div>
""",
    unsafe_allow_html=True,
)

# ---------------- THANH CHỈ SỐ ----------------
st.write("📊 **Chỉ số sinh hoạt:**")

st.caption(f"🐟 Độ no: {st.session_state.hunger}%")
st.progress(st.session_state.hunger / 100)

st.caption(f"💖 Độ vui: {st.session_state.happiness}%")
st.progress(st.session_state.happiness / 100)

st.caption(f"⚡ Năng lượng: {st.session_state.energy}%")
st.progress(st.session_state.energy / 100)

st.divider()

# ---------------- NÚT HÀNH ĐỘNG ----------------
st.write("🎮 **Hành động với mèo:**")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🐟 Cho ăn cá", use_container_width=True):
        if st.session_state.hunger >= 100:
            st.warning(f"{st.session_state.cat_name} đã no căng bụng rồi!")
        else:
            st.session_state.hunger = min(100, st.session_state.hunger + 25)
            st.session_state.energy = max(0, st.session_state.energy - 5)
            gain_exp(15)
            st.toast(
                f"Măm măm! {st.session_state.cat_name} ăn cá ngon lành!",
                icon="🐟",
            )
            st.rerun()

with col2:
    if st.button("🐾 Vuốt ve", use_container_width=True):
        if st.session_state.energy <= 10:
            st.warning(f"{st.session_state.cat_name} mệt quá rồi, hãy cho đi ngủ!")
        else:
            st.session_state.happiness = min(
                100, st.session_state.happiness + 20
            )
            st.session_state.energy = max(0, st.session_state.energy - 10)
            st.session_state.hunger = max(0, st.session_state.hunger - 5)
            gain_exp(20)
            st.toast(f"Purr... {st.session_state.cat_name} rất thích!", icon="💖")
            st.rerun()

with col3:
    if st.button("💤 Đi ngủ", use_container_width=True):
        if st.session_state.energy >= 100:
            st.warning(f"{st.session_state.cat_name} chưa hề buồn ngủ đâu!")
        else:
            st.session_state.energy = 100
            st.session_state.hunger = max(0, st.session_state.hunger - 20)
            gain_exp(10)
            st.toast(
                f"Khò khò... {st.session_state.cat_name} đã ngủ dậy tràn đầy năng lượng!",
                icon="😴",
            )
            st.rerun()

col4, col5 = st.columns(2)

with col4:
    if st.button("🧶 Chơi cuộn len", use_container_width=True):
        if st.session_state.energy <= 15:
            st.warning(f"{st.session_state.cat_name} mệt quá rồi, cần đi ngủ!")
        else:
            found_coins = random.randint(5, 20)
            st.session_state.coins += found_coins
            st.session_state.happiness = min(
                100, st.session_state.happiness + 25
            )
            st.session_state.energy = max(0, st.session_state.energy - 20)
            st.session_state.hunger = max(0, st.session_state.hunger - 15)
            gain_exp(25)
            st.toast(
                f"Chơi vui quá! Bạn nhặt được {found_coins} 💰!", icon="🧶"
            )
            st.rerun()

with col5:
    if st.button("🔄 Làm mới trạng thái", use_container_width=True):
        st.session_state.hunger = max(0, st.session_state.hunger - 5)
        st.session_state.happiness = max(0, st.session_state.happiness - 5)
        st.session_state.energy = max(0, st.session_state.energy - 5)
        st.rerun()
