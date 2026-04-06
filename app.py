def classify_stock():
    print("📈 Stock Analysis running....")
    try:
        eps = float(input("EPS Growth (%): "))
        de = float(input("Debt/Equity: "))
        roe = float(input("ROE (%): "))
        pe = float(input("P/E Ratio: "))
    except ValueError:
        print("Invalid input.")
        return

 
    if eps < 0 or de < 0 or roe < 0 or pe < 0:
        print("Invalid financial values.")
        return

    if eps >= 15 and roe >= 18 and de <= 1:
        if pe <= 20:
            result = "Strong Buy (Growth + Value)"
        else:
            result = "Buy (Strong company but expensive)"
    
    elif eps >= 10 and roe >= 15 and de <= 1.5:
        if pe <= 25:
            result = "Buy"
        else:
            result = "Hold (Valuation high)"

    elif de > 2:
        result = "Avoid (High Debt Risk)"

    elif pe > 30:
        result = "Avoid (Overvalued Stock)"

    else:
        result = "Hold / Watchlist"

    print(f"\n📊 Recommendation: {result}")


if __name__ == "__main__":
    classify_stock()