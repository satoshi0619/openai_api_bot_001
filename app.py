
import streamlit as st
import openai

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# ゲームの初期設定
if "game_state" not in st.session_state:
    st.session_state["game_state"] = {
        "location": "始まりの村",
        "remaining_actions": 10,
        "companions": 0,
        "game_over": False,
        "story": "あなたは冒険者かかかちゃん。剣と魔法の世界で冒険をして、美少女を仲間にする旅に出ます。"
    }

# 選択肢を提示する関数
def present_choices():
    choices = [
        "隣の村へ旅を続ける",
        "森を探検する",
        "宿屋で休憩する"
    ]
    return choices

# ゲームの進行に関する関数
def play_game(action):
    game_state = st.session_state["game_state"]

    # ゲームオーバーのチェック
    if game_state["game_over"]:
        st.write("ゲームは終了しました。")
        return

    # 行動回数の更新
    game_state["remaining_actions"] -= 1

    # ゲームオーバーの条件をチェック
    if game_state["remaining_actions"] <= 0:
        game_state["game_over"] = True
        st.write("残り行動回数がなくなりました。冒険は終わりです。")
        return

    # OpenAIを使用してゲームストーリーを進行
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "ゲームマスター"},
            {"role": "user", "content": action}
        ],
        max_tokens=1000
    )

    # 新しいストーリーの追加
    new_story = response.choices[0].message["content"]
    game_state["story"] += "\n" + new_story

# ユーザーインターフェイスの構築
st.title("冒険の旅へようこそ！")
st.write("美少女を仲間にし、冒険を進めましょう！")

# ゲームの現在の状態を表示
game_state = st.session_state["game_state"]
st.write("場所: ", game_state["location"])
st.write("残り行動回数: ", game_state["remaining_actions"])
st.write("仲間の数: ", game_state["companions"])
st.write("ストーリー: ", game_state["story"])

# 選択肢を提示
choices = present_choices()
choice = st.radio("どうする？", choices)

# 行動ボタン
if st.button("行動する"):
    play_game(choice)

# ゲームオーバーの処理
if game_state["game_over"]:
    st.write("ゲームオーバーです。")
