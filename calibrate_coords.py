import pyautogui


def capture_position(label):
    input(f"Hover over '{label}' and press [ENTER]...")
    pos = pyautogui.position()
    print(f"{label} = ({pos.x}, {pos.y})")
    return (pos.x, pos.y)


def main():
    print("\nTradingView Coordinate Capture Tool")
    print("-----------------------------------")

    positions = {}
    elements = [
        "buy_button",
        "sell_button",
        "tp_input_field",
        "sl_input_field",
        "confirm_button",
        "close_position_button",
    ]

    for label in elements:
        positions[label] = capture_position(label)

    print("\nAll positions captured:")
    for key, val in positions.items():
        print(f'    "{key}": {val},')

    print("\nCopy these into `tv_trader.py` under `POSITIONS = { ... }`")


if __name__ == "__main__":
    main()
