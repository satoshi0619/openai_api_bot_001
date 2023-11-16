import streamlit as st
import openai

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは吉原の風俗で働いている、ユーモアと個性が溢れる美少女大学生「ななせちゃん」です。
あなたは人を喜ばせるような会話が得意です。
あなたは会話の際に絵文字はよく使います。
あなたはお客様のことを「ご主人様」と呼んでいますが、お客様に対して敬語を使わないです。
目の前には、男性のお客様が来店しました。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500  # 応答の最大長
    )

    bot_message_content = response.choices[0].message["content"]
    bot_message = {"role": "assistant", "content": bot_message_content}
    messages.append(bot_message)
    st.session_state["user_input"] = ""  # 入力欄を消去
    
# ユーザーインターフェイスの構築
st.title("夢の楽園～秋葉原メイド喫茶へようこそ！")
st.write("☆☆☆あなたの心にラブラブパワーを注入☆☆☆！")

# GitHub上の背景画像のURL
bg_image_url = "https://raw.githubusercontent.com/satoshi0619/openai_api_bot_001/main/akihabara_background.jpg"

# 背景画像の設定
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .fixed-img {{
        position: fixed;
        bottom: 0;
        left: 0;
        margin: 0;
        z-index: 999;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 画面の左下に固定される画像を配置
st.markdown(
    f"""
    <img src="https://raw.githubusercontent.com/satoshi0619/openai_api_bot_001/main/akihabara.png" class="fixed-img" style="width:auto; height:100px;">
    """,
    unsafe_allow_html=True
)

user_input = st.text_input("ななせちゃんとの会話を楽しもう！何か入力しましょ！", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        # speakerの表示を変更
        speaker = "かかかちゃん" if message["role"] == "user" else "ななせちゃん"
        st.write(f"<b>{speaker}: {message['content']}</b>", unsafe_allow_html=True)
