import streamlit as st

# --- パスコードを Secrets から読み込む ---
PASSWORD = st.secrets["app_password"]  # ← Secretsに設定した値を読み込む

# --- セッション状態の初期化 ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- パスコード未入力時 ---
if not st.session_state["authenticated"]:
    st.title("🔒 パスコード認証ページ")
    password_input = st.text_input("パスコードを入力してください", type="password")

    if st.button("入室"):
        if password_input == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("認証に成功しました！")
            st.experimental_rerun()
        else:
            st.error("パスコードが違います。もう一度入力してください。")

# --- 認証後のページ ---
else:
    # ページタイトル
    st.title("株の利確ラインどうする？")
    st.subheader("「テキトーにエントリーしたけど利確ラインどうしよう…」")
    
    st.text("取得株価と株数を入力すると2%,3%,5%の上昇・下落時にいくらの損益になるかを自動表示します。\n利確・損切りタイミングの参考にどうぞ。")
    # 入力欄（横並び）
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("取得株価（円）を入力してください", min_value=0, value=100, step=1)
    with col2:
        quantity = st.number_input("取得株数（株）を入力してください", min_value=0, value=100, step=1)
    # 増減率とラベル
    ratios = [1.01,1.02, 1.03, 1.05, 0.99, 0.98, 0.97, 0.95]
    labels = ["＋1％", "＋2％", "＋3％", "＋5％", "－1％", "－2％", "－3％", "－5％"]
    
    # 結果表示
    st.markdown("### 💹 計算結果")
    
    if price > 0 and quantity > 0:
        for label, ratio in zip(labels, ratios):
            new_price = int(price * ratio)
            diff = (new_price - price) * quantity #実際の損益額
            formatted_price = f"{new_price:,}"
            formatted_diff = f"{diff:+,}" #正負を明示して３桁区切り
            
            if ratio > 1:  # 上昇
                st.markdown(
                    f'{label}：<span style="color:coral;">{formatted_price} 円　　</span>'
                    f' |　　損益：<span style="color:coral;">{formatted_diff} 円　　</span>', 
                    unsafe_allow_html=True
                )
            else:  # 下落            
                st.markdown(
                    f'{label}：<span style="color:deepskyblue;">{formatted_price} 円　　</span>'
                    f' |　　損益：<span style="color:deepskyblue;">{formatted_diff} 円　　</span>', 
                    unsafe_allow_html=True
                )
    else:
        st.info("💡 取得株価と株数を入力すると結果が表示されます。")
        
    st.text("\n\nPythonの勉強で作ったテストページです。\n2025.11.8\n「株の利確ラインどうする？ver.3」")

    # ログアウトボタン    
    if st.button("ログアウト"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
