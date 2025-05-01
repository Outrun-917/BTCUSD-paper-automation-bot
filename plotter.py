# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# # import tkinter as Tk

# def plot_chart(df, signal=None):
#     plt.close()
    
#     df = df.copy().dropna().tail(60)  # Plot last 60 candles

#     fig, (ax_price, ax_rsi) = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
#     fig.suptitle('BTC/USD Scalper Strategy View')
    
#     # Get current window manager
#     manager = plt.get_current_fig_manager()
#     window = manager.window

#     # Move the window to the second screen (e.g., screen 1, change coordinates as needed)
#     window.geometry('-2560+0')  # Assuming 1920x1080 resolution for the first screen

#     # --- Price Chart with Bollinger Bands & VWAP
#     ax_price.plot(df.index, df["close"], label="Close", color="black", linewidth=1)
#     ax_price.plot(df.index, df["bb_upper"], label="BB Upper", linestyle='--', color="red", linewidth=0.8)
#     ax_price.plot(df.index, df["bb_lower"], label="BB Lower", linestyle='--', color="green", linewidth=0.8)
#     ax_price.plot(df.index, df["vwap"], label="VWAP", color="blue", linewidth=0.8)

#     # --- Signal Markers
#     if signal == "long":
#         ax_price.scatter(df.index[-1], df["close"].iloc[-1], color='green', marker='^', s=80, label="Buy Signal")
#     elif signal == "short":
#         ax_price.scatter(df.index[-1], df["close"].iloc[-1], color='red', marker='v', s=80, label="Sell Signal")

#     ax_price.legend(loc="upper left")
#     ax_price.set_ylabel("Price (USD)")
#     ax_price.grid(True)

#     # --- RSI subplot
#     ax_rsi.plot(df.index, df["rsi"], label="RSI", color="purple", linewidth=0.8)
#     ax_rsi.axhline(70, color="red", linestyle="--", linewidth=0.6)
#     ax_rsi.axhline(30, color="green", linestyle="--", linewidth=0.6)
#     ax_rsi.set_ylabel("RSI")
#     ax_rsi.set_ylim(0, 100)
#     ax_rsi.grid(True)

#     ax_rsi.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

#     plt.tight_layout()
#     plt.pause(0.01)  
#     plt.clf()
