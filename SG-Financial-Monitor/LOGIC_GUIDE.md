*This file teaches the user exactly how your "Analytical Brain" works.*
# 🔍 How the Analytical Brain Works
The SG Financial Monitor doesn't just "fetch" prices; it processes them through a mathematical pipeline to provide context. Here is the step-by-step logic.
### 1. The RSI Calculation (14-Period Hourly)
The bot uses the **Relative Strength Index (RSI)**, a momentum oscillator that measures the speed and change of price movements.
**The Process:**
 * **Data Retrieval:** The bot pulls the last 100 hours of "Closing Prices" from the Binance API.
 * **Calculating "Deltas":** It finds the difference between each hour's closing price and the one before it.
 * **Gain/Loss Separation:** * If the price went up, that's a **Gain**.
   * If the price went down, that's a **Loss**.
 * **Rolling Average:** It calculates the average gain and average loss over the last **14 periods** (hours).
 * **Relative Strength (RS):** 
 * **Final RSI Formula:**
   
### 2. Strategic Intelligence Labeling
Once the RSI is calculated, the get_strategy_label function categorizes the asset:
 * **RSI > 70:** Market is "Overbought." Buyers are exhausted; a pullback is statistically likely.
 * **RSI < 30:** Market is "Oversold." Sellers are exhausted; a price "bounce" is expected.
 * **30 - 70:** Market is "Stable." Momentum is neutral.
### 3. Range Position (Daily Context)
To understand if a price is at a "ceiling" or a "floor," the bot calculates the **Range Position**:

 * **> 85%:** The asset is testing **Resistance** (Top of the daily range).
 * **< 15%:** The asset is testing **Support** (Bottom of the daily range).
