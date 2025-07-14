import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Data loader ---
def load_data(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1y")
    if df.empty:
        raise ValueError("No data found.")
    df["Return"] = df["Close"].pct_change()
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df["Label"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df.dropna(inplace=True)
    return df, ticker

# --- ML Predictor ---
def predict(df):
    X = df[["Return", "MA5", "MA10"]]
    y = df["Label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    pred_proba = model.predict_proba([X.iloc[-1]])[0]
    pred = int(pred_proba[1] > 0.5)
    confidence = pred_proba[1] if pred == 1 else pred_proba[0]
    accuracy = model.score(X_test, y_test)
    expected_change = df["Return"].tail(10).mean() * 100
    return pred, confidence, accuracy, expected_change

# --- Streamlit UI ---
st.set_page_config(page_title="AI Market Predictor", layout="centered")
st.title("📈 AI Stock & Crypto Predictor")
st.caption("Enter any valid stock or crypto symbol (like `AAPL`, `TSLA`, `ETH`, `BTC`, `SHIB`, etc.)")

market = st.radio("Market Type", ["Stock", "Crypto"], horizontal=True)


# --- Input Section ---
st.markdown("### 🔎 Enter a symbol to predict")
user_input = st.text_input("Enter symbol:", placeholder="e.g. AAPL, TSLA, BTC, ETH").strip().upper()

# Fix crypto format if needed
if market == "Crypto" and user_input and not user_input.endswith("-USD"):
    symbol = f"{user_input}-USD"
else:
    symbol = user_input

if symbol:
    try:
        with st.spinner("Loading data and making prediction..."):
            df, ticker = load_data(symbol)
            if df.shape[0] < 30:
                st.warning("Not enough data for prediction. Try another symbol.")
            else:
                pred, confidence, accuracy, expected_change = predict(df)
                live_price = ticker.info.get("regularMarketPrice", "N/A")
                prev_close = ticker.info.get("previousClose", "N/A")
                vol = ticker.info.get("volume", "N/A")
                high52 = ticker.info.get("fiftyTwoWeekHigh", "N/A")
                low52 = ticker.info.get("fiftyTwoWeekLow", "N/A")

                # Chart
                st.subheader(f"📊 Price Chart for {symbol}")
                st.line_chart(df["Close"])

                # Prediction Section
                direction = "⬆️ UP" if pred == 1 else "⬇️ DOWN"
                st.markdown(f"## 🧠 Prediction: **{direction}**")
                st.info(f"Confidence: **{confidence*100:.2f}%**")
                st.success(f"Expected Change (next day): **{expected_change:.2f}%**")
                st.warning(f"Model Accuracy (last 20%): **{accuracy*100:.2f}%**")

                # Current Price
                if isinstance(live_price, (float, int)):
                    st.markdown(f"### 💰 Current Price: **${live_price:.2f}**")
                else:
                    st.markdown("### 💰 Current Price: Unavailable")

                # Extra Stats
                st.divider()
                st.markdown("### 📌 Extra Market Info")
                col1, col2 = st.columns(2)
                with col1:
                    if isinstance(prev_close, (float, int)):
                        st.metric("Previous Close", f"${prev_close:.2f}")
                    if isinstance(high52, (float, int)):
                        st.metric("52-Week High", f"${high52:.2f}")
                with col2:
                    if isinstance(vol, int):
                        st.metric("Volume", f"{vol:,}")
                    if isinstance(low52, (float, int)):
                        st.metric("52-Week Low", f"${low52:.2f}")

    except ValueError as ve:
        st.error(f"❌ {ve}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
