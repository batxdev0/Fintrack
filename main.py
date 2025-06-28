print("✅ STARTING SCRIPT...")

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def get_price_data(coin="bitcoin", days=30):
    print("🔄 Fetching price data...")
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    r = requests.get(url, params=params)
    
    if r.status_code != 200:
        print(f"❌ Failed to fetch: {r.status_code}")
        return pd.DataFrame()

    data = r.json()["prices"]
    df = pd.DataFrame(data, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
    df = df.groupby("date").mean().reset_index()
    return df

def analyze_price(df):
    print("📊 Running analysis...")
    start = df["price"].iloc[0]
    end = df["price"].iloc[-1]
    change = ((end - start) / start) * 100
    avg = df["price"].mean()
    std = df["price"].std()
    print(f"Start: ${start:.2f}")
    print(f"End: ${end:.2f}")
    print(f"Change: {change:.2f}%")
    print(f"Average: ${avg:.2f}")
    print(f"Volatility: ±${std:.2f}")

def plot_price(df, coin):
    print("📈 Plotting...")
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["price"], marker='o', color='orange')
    plt.xticks(rotation=45)
    plt.grid()
    filename = f"assets/{coin}_plot.png"
    plt.savefig(filename)
    plt.show()
    print(f"[✅] Saved plot to {filename}")

if __name__ == "__main__":
    print("🚀 Running main...")
    df = get_price_data("bitcoin", 30)

    if df.empty:
        print("❌ No data.")
    else:
        analyze_price(df)
        plot_price(df, "bitcoin")

