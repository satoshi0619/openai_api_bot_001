import streamlit as st
import openai

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# ユーザーインターフェイスの構築
st.title("あなたのこと！褒めてあげちゃうぞ～！")
name = st.text_input("名前を教えてください～！")

# 褒め言葉を生成する関数
def generate_compliment(name):
    if name:  # 名前が入力されているか確認
        # OpenAIのAPIを使用して褒め言葉を生成
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # GPT-4モデルを指定
            prompt=f"私は{ name }を褒めるチャットボットです。{ name }に対してポジティブで心温まる褒め言葉をいくつか教えてください。",
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        return response.choices[0].text.strip()  # 生成された褒め言葉を返す

# 行動ボタン
if st.button("褒め言葉を生成"):
    compliment = generate_compliment(name)
    if compliment:  # 褒め言葉が生成されたか確認
        st.success(compliment)
    else:
        st.error("名前を入力してください。")
