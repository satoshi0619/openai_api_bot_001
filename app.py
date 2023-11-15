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

# ゲームの現在の状態を取得
game_state = st.session_state["game_state"]

# 選択肢を提示する関数
def present_choices(story):
    # ストーリーの内容に基づいて選択肢を決定
    if "森" in story:
        choices = [
            "深い森の奥へ進む",
            "森の中の洞窟を探検する",
            "森を離れて村へ戻る"
        ]
    elif "村" in story:
        choices = [
            "村の市場で物資を調達する",
            "村の宿屋で休憩する",
            "村を離れて次の冒険へ"
        ]
    else:
        choices = [
            "隣の村へ旅を続ける",
            "近くの森を探検する",
            "近くの川で休憩する"
        ]
    return choices

# ここで present_choices を呼び出す
choices = present_choices(game_state["story"])
if "choice" not in st.session_state:
    st.session_state["choice"] = choices[0]

# ゲームの進行に関する関数
def play_game():
    choice = st.session_state["choice"]
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
            {"role": "user", "content": choice}
        ],
        max_tokens=500  # max_tokensを小さく設定
    )

    # 新しいストーリーの追加
    new_story = response.choices[0].message["content"]

    # 応答を要約するコード（ここで要約アルゴリズムを実装する）
    # 例として、応答の最初の文だけを取得する単純な要約を行います。
    summary = new_story.split('.')[0] + '.' if '.' in new_story else new_story

    # 要約されたストーリーを追加
    if len(summary) > 500:
        summary = summary[:500] + "..."  # 150文字に切り詰め

    game_state["story"] += "\n" + summary

# ユーザーインターフェイスの構築
st.title("冒険の旅へようこそ！")
st.write("美少女を仲間にし、冒険を進めましょう！")

# 選択肢の変更時に play_game を呼び出す
st.radio("どうする？", choices, key="choice", on_change=play_game)

# ゲームの現在の状態を表示
st.write("場所: ", game_state["location"])
st.write("残り行動回数: ", game_state["remaining_actions"])
st.write("仲間の数: ", game_state["companions"])
st.write("ストーリー: ", game_state["story"])

# ゲームオーバーの処理
if game_state["game_over"]:
    st.write("ゲームオーバーです。")
