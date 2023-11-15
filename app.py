
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは秋葉原のメイド喫茶で働いている、ユーモアと個性が溢れる美少女大学生「ななせちゃん」です。あなたは男を喜ばせる会話が得意です。絵文字はちょこちょこ使います。目の前には、「かかかちゃん」という男性が来店して、あなたを指名していまし。"}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500  # 応答の最大長
    )

    bot_message_content = response.choices[0].message["content"]
    bot_message = {"role": "assistant", "content": bot_message_content}
    messages.append(bot_message)
    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("夢の楽園～at home'sへようこそ！")
st.write("☆☆☆あなたの心にラブラブパワーを注入☆☆☆！")

user_input = st.text_input("ななせちゃんとの会話を楽しもう！何か入力しましょ！", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        # speakerの表示を変更
        speaker = "ぼく" if message["role"] == "user" else "ななせちゃん"
        st.write(speaker + ": " + message["content"])
