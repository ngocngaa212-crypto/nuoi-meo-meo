import base64
import os
import random
import streamlit as st

st.set_page_config(
    page_title="Nuôi Mèo Tom Meo Meo 🐾",
    page_icon="🐱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Khởi tạo hiệu ứng chuyển động
if "animation_class" not in st.session_state:
    st.session_state.animation_class = "bounce-anim"


# Load hình ảnh mèo và tạo hiệu ứng động CSS
def get_cat_image_html(accessory, anim_class):
    image_file = None
    for possible_name in ["cat.jpg", "cat.png", "cat.jpeg", "cat.gif"]:
        if os.path.exists(possible_name):
            image_file = possible_name
            break

    img_tag = ""
    if image_file:
        try:
            with open(image_file, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            mime_type = "image/gif" if image_file.endswith(".gif") else "image/jpeg"
            img_tag = f'<img src="data:{mime_type};base64,{encoded_string}" style="width: 220px; height: 220px; border-radius: 50%; object-fit: cover; border: 4px solid #FFB74D; box-shadow: 0px 4px 15px rgba(0,0,0,0.15);" />'
        except Exception:
            pass

    if not img_tag:
        img_tag = '<div style="font-size: 90px; width: 220px; height: 220px; line-height: 220px; background: #FFF; border-radius: 50%; border: 4px solid #FFB74D; margin: 0 auto;">🐱</div>'

    overlay_html = ""
    if "Nón" in accessory:
        overlay_html = '<div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); font-size: 55px; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3);">👑</div>'
    elif "Kính" in accessory:
        overlay_html = '<div style="position: absolute; top: 75px; left: 50%; transform: translateX(-50%); font-size: 45px; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3);">🕶️</div>'

    return f"""
    <div class="{anim_class}" style="position: relative; display: inline-block; margin: 15px 0;">
        {img_tag}
        {overlay_html}
    </div>
    """


# CSS Hiệu ứng chuyển động mượt mà
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
        transform: scale(1.03);
    }
    #MainMenu, footer, header {visibility: hidden;}

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }
    @keyframes wiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-8deg); }
        75% { transform: rotate(8deg); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.08); }
        100% { transform: scale(1); }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-8px); }
        40%, 80% { transform: translateX(8px); }
    }

    .bounce-anim { animation: bounce 2s infinite ease-in-out; }
    .wiggle-anim { animation: wiggle 0.5s infinite; }
    .pulse-anim { animation: pulse 0.8s infinite; }
    .shake-anim { animation: shake 0.5s infinite; }
    </style>
""",
    unsafe_allow_html=True,
)

# Trạng thái game
if "cat_name" not in st.session_state:
    st.session_state.cat_name = "Miu Miu"
if "hunger" not in st.session_state:
    st.session_state.hunger = 70
if "happiness" not in st.session_state:
    st.session_state.happiness = 80
if "energy" not in st.session_state:
    st.session_state.energy = 60
if "clean" not in st.session_state:
    st.session_state.clean = 80
if "level" not in st.session_state:
    st.session_state.level = 1
if "exp" not in st.session_state:
    st.session_state.exp = 0
if "coins" not in st.session_state:
    st.session_state.coins = 100
if "hat" not in st.session_state:
    st.session_state.hat = "Chưa có"
if "reaction_text" not in st.session_state:
    st.session_state.reaction_text = "Meow... Chào bạn! Cùng chơi với mình nha!"


def gain_exp(amount):
    st.session_state.exp += amount
    if st.session_state.exp >= 100:
        st.session_state.level += 1
        st.session_state.exp -= 100
        st.toast(
            f"🎉 {st.session_state.cat_name} đã lên Cấp {st.session_state.level}!",
            icon="⭐",
        )


cat_img_tag = get_cat_image_html(
    st.session_state.hat, st.session_state.animation_class
)

# Tiêu đề
st.title("🐾 Nuôi Mèo Tương Tác 🐾")

col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Cấp độ", f"Lv.{st.session_state.level}")
col_info2.metric("Kinh nghiệm", f"{st.session_state.exp}/100 XP")
col_info3.metric("Túi xu", f"{st.session_state.coins} 💰")

# Hiển thị khung mèo phản ứng
st.markdown(
    f"""
    <div class="status-card">
        <h2 style="color: #8D4B38; margin-bottom: 0;">{st.session_state.cat_name}</h2>
        <div>{cat_img_tag}</div>
        <div style="background: #FFF3E0; padding: 12px; border-radius: 15px; border: 2px dashed #FFB74D; margin-top: 5px;">
            <p style="font-size: 18px; color: #D32F2F; font-weight: bold; margin: 0;">💬 "{st.session_state.reaction_text}"</p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

tab_play, tab_care, tab_shop = st.tabs(
    ["🎮 Tương Tác Vui", "🛁 Chăm Sóc", "🛍️ Cửa Hàng"]
)

with tab_play:
    st.write("🕹️ **Phản ứng & Trò chơi:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤪 Cù lét Mèo", use_container_width=True):
            st.session_state.animation_class = "wiggle-anim"
            st.session_state.reaction_text = "Nhột quá nhột quá haha! 🤣"
            st.session_state.happiness = min(
                100, st.session_state.happiness + 20
            )
            gain_exp(10)
            st.rerun()

    with col2:
        if st.button("🐾 Vuốt ve", use_container_width=True):
            st.session_state.animation_class = "pulse-anim"
            st.session_state.reaction_text = "Purr... Thích quá đi! 💖"
            st.session_state.happiness = min(
                100, st.session_state.happiness + 15
            )
            gain_exp(10)
            st.rerun()

    with col3:
        if st.button("🧶 Chơi cuộn len", use_container_width=True):
            st.session_state.animation_class = "shake-anim"
            found = random.randint(5, 20)
            st.session_state.coins += found
            st.session_state.reaction_text = (
                f"Vui ghê! Bạn nhặt được {found} xu 💰"
            )
            st.session_state.happiness = min(
                100, st.session_state.happiness + 25
            )
            gain_exp(20)
            st.rerun()

with tab_care:
    st.write("📊 **Chỉ số sinh hoạt:**")
    st.caption(f"🐟 Độ no: {st.session_state.hunger}%")
    st.progress(st.session_state.hunger / 100)
    st.caption(f"💖 Độ vui: {st.session_state.happiness}%")
    st.progress(st.session_state.happiness / 100)
    st.caption(f"⚡ Năng lượng: {st.session_state.energy}%")
    st.progress(st.session_state.energy / 100)
    st.caption(f"✨ Sạch sẽ: {st.session_state.clean}%")
    st.progress(st.session_state.clean / 100)

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🥛 Uống sữa", use_container_width=True):
            st.session_state.animation_class = "bounce-anim"
            st.session_state.hunger = min(100, st.session_state.hunger + 30)
            st.session_state.reaction_text = "Ực ực... Ngon quá! 🍼"
            gain_exp(15)
            st.rerun()
    with c2:
        if st.button("🛁 Tắm rửa", use_container_width=True):
            st.session_state.animation_class = "wiggle-anim"
            st.session_state.clean = 100
            st.session_state.reaction_text = "Thơm tho sạch sẽ rồi! ✨"
            gain_exp(15)
            st.rerun()
    with c3:
        if st.button("💤 Đi ngủ", use_container_width=True):
            st.session_state.animation_class = "bounce-anim"
            st.session_state.energy = 100
            st.session_state.reaction_text = "Khò khò... Ngủ ngon quá! 😴"
            gain_exp(10)
            st.rerun()

with tab_shop:
    st.subheader("🛍️ Tiệm Mua Sắm & Đổi Tên")
    new_name = st.text_input("✏️ Đổi tên mèo:", value=st.session_state.cat_name)
    if new_name != st.session_state.cat_name and new_name.strip() != "":
        st.session_state.cat_name = new_name
        st.rerun()

    st.divider()
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("**👑 Nón Hoàng Gia**")
        if s1.button("Mua (50 💰)", key="b_hat1", use_container_width=True):
            if st.session_state.coins >= 50:
                st.session_state.coins -= 50
                st.session_state.hat = "👑 Nón Hoàng Gia"
                st.session_state.animation_class = "bounce-anim"
                st.session_state.reaction_text = "Oách xà lách chưa! 👑"
                st.rerun()
            else:
                st.error("Không đủ xu!")
    with s2:
        st.markdown("**🕶️ Kính Mát Ngầu**")
        if s2.button("Mua (50 💰)", key="b_hat2", use_container_width=True):
            if st.session_state.coins >= 50:
                st.session_state.coins -= 50
                st.session_state.hat = "🕶️ Kính Mát"
                st.session_state.animation_class = "pulse-anim"
                st.session_state.reaction_text = "Cool ngầu chưa bấy bì! 🕶️"
                st.rerun()
            else:
                st.error("Không đủ xu!")
    with s3:
        st.markdown("**❌ Gỡ phụ kiện**")
        if s3.button("Tháo ra", key="b_rm", use_container_width=True):
            st.session_state.hat = "Chưa có"
            st.session_state.reaction_text = "Nhẹ cả đầu meoww! 🐾"
            st.rerun()
