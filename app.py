import streamlit as st
import openai

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# ユーザーインターフェイスの構築
st.title("あなたのことを褒めてあげちゃうぞ〜！")
name = st.text_input("名前を教えてください〜！")

# 褒め言葉を生成する関数
def generate_compliment(name):
    if name:  # 名前が入力されているか確認
        try:
            # OpenAIのChat APIを使用して褒め言葉を生成
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # モデルを指定
                messages=[
                    {"role": "system", "content": "あなたは人を褒め言葉が上手なロボットです"},
                    {"role": "user", "content": f"私のことをいっぱい褒めてください! 私の名前は {name}."}
                ],
                max_tokens=60
            )
            return response.choices[0].message["content"].strip()  # 生成された褒め言葉を返す
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI APIでエラーが発生しました: {e}")
            return None
    else:
        return None  # 名前が入力されていなければNoneを返す

# 行動ボタン
if st.button("褒め言葉を生成"):
    compliment = generate_compliment(name)
    if compliment:  # 褒め言葉が生成されたか確認
        st.success(compliment)
    else:
        st.error("名前を入力して、もう一度試してください。")
