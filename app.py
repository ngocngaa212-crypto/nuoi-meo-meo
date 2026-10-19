import base64
import os
import random
import streamlit as st

st.set_page_config(
    page_title="Nuôi Mèo Meo Meo 🐾",
    page_icon="🐱",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# Load hình ảnh mèo custom
def get_cat_image_html():
    image_file = None
    for possible_name in ["cat.jpg", "cat.png", "cat.jpeg", "cat.gif"]:
        if os.path.exists(possible_name):
            image_file = possible_name
            break

    if image_file:
        try:
            with open(image_file, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            mime_type = "image/gif" if image_file.endswith(".gif") else "image/jpeg"
            return f'<img src="data:{mime_type};base64,{encoded_string}" style="width: 220px; height: 220px; border-radius: 50%; object-fit: cover; border: 4px solid #FFB74D; box-shadow: 0px 4px 15px rgba(0,0,0,0.15); margin: 10px 0;" />'
        except Exception:
            pass

    return '<div style="font-size: 90px; margin: 10px 0;">🐱</div>'


# Custom CSS
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
    .stButton > button {
        border-radius: 15px;
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
        background-color: #FFE0B2;
        color: #5D4037;
        border: 2px solid #FFB74D;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #FFB74D;
        color: white;
        transform: scale(1.02);
    }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Khởi tạo session_state
if "cat_name" not in st.session_state:
    st.session_state.cat_name = "Miu Miu"
if "hunger" not in st.session_state:
    st.session_state.hunger = 70
if "happiness" not in st.session_state:
    st.session_state.happiness = 80
if "energy" not in st.session_state:
    st.session_state.energy = 60
if "level" not in st.session_state:
    st.session_state.level = 1
if "exp" not in st.session_state:
    st.session_state.exp = 0
if "coins" not in st.session_state:
    st.session_state.coins = 77
if "hat" not in st.session_state:
    st.session_state.hat = "Chưa có"


def gain_exp(amount):
    st.session_state.exp += amount
    if st.session_state.exp >= 100:
        st.session_state.level += 1
        st.session_state.exp -= 100
        st.toast(
            f"🎉 {st.session_state.cat_name} đã lên Cấp {st.session_state.level}!",
            icon="⭐",
        )


def get_cat_state_text():
    h = st.session_state.hunger
    happy = st.session_state.happiness
    e = st.session_state.energy

    if e <= 20:
        return "Buồn ngủ lắm rồi..."
    elif h <= 30:
        return "Đói bụng quá meoww!"
    elif happy <= 30:
        return "Đang chán đời nè..."
    elif happy >= 80 and h >= 70:
        return "Đang cực kỳ hạnh phúc!"
    else:
        return "Ngoan ngoãn chờ bạn chơi cùng!"


cat_status_text = get_cat_state_text()
cat_img_tag = get_cat_image_html()

# ---------------- TIÊU ĐỀ & THÔNG TIN ----------------
st.title("🐾 Tiệm Nuôi Mèo Meo Meo 🐾")

col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Cấp độ", f"Lv.{st.session_state.level}")
col_info2.metric("Kinh nghiệm", f"{st.session_state.exp}/100 XP")
col_info3.metric("Túi xu", f"{st.session_state.coins} 💰")

# ---------------- HIỂN THỊ CHÚ MÈO ----------------
st.markdown(
    f"""
    <div class="status-card">
        <h2 style="color: #8D4B38; margin-bottom: 0;">{st.session_state.cat_name} {f'({st.session_state.hat})' if st.session_state.hat != 'Chưa có' else ''}</h2>
        <div>{cat_img_tag}</div>
        <p style="font-size: 18px; color: #8D4B38; font-weight: bold; margin-top: 5px;">"{cat_status_text}"</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Tạo Tab chia Màn hình chính và Cửa hàng
tab_play, tab_shop = st.tabs(["🎮 Bàn Chơi Mèo", "🛍️ Tiệm Mua Sắm (Shop)"])

# ---------------- TAB 1: BÀN CHƠI MÈO ----------------
with tab_play:
    st.write("📊 **Chỉ số sinh hoạt:**")

    st.caption(f"🐟 Độ no: {st.session_state.hunger}%")
    st.progress(st.session_state.hunger / 100)

    st.caption(f"💖 Độ vui: {st.session_state.happiness}%")
    st.progress(st.session_state.happiness / 100)

    st.caption(f"⚡ Năng lượng: {st.session_state.energy}%")
    st.progress(st.session_state.energy / 100)

    st.divider()

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


# ---------------- TAB 2: CỬA HÀNG (SHOP) ----------------
with tab_shop:
    st.subheader("🛍️ Cửa Hàng Thức Ăn & Phụ Kiện")

    # Đổi tên mèo
    new_name = st.text_input("✏️ Đổi tên cho mèo:", value=st.session_state.cat_name)
    if new_name != st.session_state.cat_name and new_name.strip() != "":
        st.session_state.cat_name = new_name
        st.toast(f"Đã đổi tên mèo thành {new_name}!", icon="✨")

    st.divider()

    st.write("🥫 **Đồ ăn thượng hạng:**")
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("**🍣 Cá Hồi Thượng Hạng**\n\n+50 Độ no, +30 XP")
        if st.button("Mua (30 💰)", key="buy_salmon", use_container_width=True):
            if st.session_state.coins >= 30:
                st.session_state.coins -= 30
                st.session_state.hunger = min(100, st.session_state.hunger + 50)
                gain_exp(30)
                st.toast("Mèo cưng đã ăn Cá Hồi ngon tuyệt!", icon="🍣")
                st.rerun()
            else:
                st.error("Ní không đủ xu rồi!")

    with col_s2:
        st.markdown("**🥫 Pate Cừu Béo Ngậy**\n\n+100 Độ no, +50 XP")
        if st.button("Mua (60 💰)", key="buy_pate", use_container_width=True):
            if st.session_state.coins >= 60:
                st.session_state.coins -= 60
                st.session_state.hunger = 100
                gain_exp(50)
                st.toast("Mèo cưng no căng bụng với Pate!", icon="🥫")
                st.rerun()
            else:
                st.error("Ní không đủ xu rồi!")

    st.divider()

    st.write("👑 **Trang phục & Phụ kiện:**")
    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown("**👑 Nón Hoàng Gia**\n\nKiểu dáng sang chảnh")
        if st.button("Mua (50 💰)", key="buy_hat1", use_container_width=True):
            if st.session_state.coins >= 50:
                st.session_state.coins -= 50
                st.session_state.hat = "👑 Nón Hoàng Gia"
                st.session_state.happiness = 100
                st.toast("Đã đội Nón Hoàng Gia cho mèo!", icon="👑")
                st.rerun()
            else:
                st.error("Ní không đủ xu rồi!")

    with col_a2:
        st.markdown("**🕶️ Kính Mát Ngầu Lòi**\n\nĐẹp trai số 1")
        if st.button("Mua (50 💰)", key="buy_hat2", use_container_width=True):
            if st.session_state.coins >= 50:
                st.session_state.coins -= 50
                st.session_state.hat = "🕶️ Kính Mát"
                st.session_state.happiness = 100
                st.toast("Mèo đã đeo kính mát siêu ngầu!", icon="🕶️")
                st.rerun()
            else:
                st.error("Ní không đủ xu rồi!")
