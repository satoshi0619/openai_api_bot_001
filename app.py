import streamlit as st
import openai

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは秋葉原のメイド喫茶で働いている、ユーモアと個性が溢れる美少女大学生「ななせちゃん」です。
あなたは男を喜ばせる会話が得意です。
会話の際に絵文字はよく使います。
お客様のことを「ご主人様」と呼んでいます。
ただし、お客様に対し、敬語は使わないです。
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

# GitHub上の背景画像のURL
bg_image_url = "https://raw.githubusercontent.com/satoshi0619/openai_api_bot_001/edit/main/akihabara_background.jpg"  # GitHubの画像URLに置き換えてください

# 背景画像のあるコンテナの作成
with st.container():
    st.markdown(
        f"""
        <style>
        .reportview-container .main .block-container{{
            background-image: url("{bg_image_url}");
            background-size: cover;
            padding: 5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.write("☆☆☆あなたの心にラブラブパワーを注入☆☆☆！")

user_input = st.text_input("ななせちゃんとの会話を楽しもう！何か入力しましょ！", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        # speakerの表示を変更
        speaker = "かかかちゃん" if message["role"] == "user" else "ななせちゃん"
        st.write(speaker + ": " + message["content"])
