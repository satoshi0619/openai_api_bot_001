import streamlit as st
import openai

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# チャットボットの感情パラメーターの初期設定
if "emotions" not in st.session_state:
    st.session_state["emotions"] = {
        "喜び": 0,
        "怒り": 0,
        "悲しみ": 0,
        "楽しさ": 0,
        "自信": 0,
        "困惑": 0,
        "恐怖": 0
    }

# ゲームの進行に関する関数
def play_game(user_input):
    emotions = st.session_state["emotions"]
    
    # 感情パラメーターの更新ロジック（ダミーの例）
    # 実際にはユーザー入力やゲームの状況に応じて感情を更新するロジックを実装する
    # ここではシンプルな例として、固定値で更新します
    emotions["喜び"] = min(emotions["喜び"] + 1, 5)
    emotions["楽しさ"] = min(emotions["楽しさ"] + 1, 5)
    
    # 感情パラメーターの表示
    st.write("&#8203;``【oaicite:1】``&#8203;")
    for emotion, value in emotions.items():
        st.write(f"{emotion}:{value}")

    # OpenAIを使用して会話を進行
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "ゲームマスター"},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150
    )
    
    # 応答の表示
    bot_response = response.choices[0].message["content"]
    st.write("&#8203;``【oaicite:0】``&#8203;")
    st.write(bot_response)

# ユーザーインターフェイスの構築
st.title("感情を持つチャットボットとの会話")

# ユーザーからの入力を受け取る
user_input = st.text_input("何を話し合いましょうか？")

# 行動ボタン
if st.button("話す"):
    play_game(user_input)
