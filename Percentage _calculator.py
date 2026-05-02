def calculate_money():
    history = []
    
    while True:
        try:
            raw_input = input("\nEnter initial amount (or 'q' to quit): ")
            if raw_input.lower() == 'q': break
            current_amount = float(raw_input)
            initial_amount = current_amount
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        print(f"\nCurrent balance: {current_amount}")
        action = input("Enter percentage to subtract (or 'b' to reset amount, 'f' to finish): ").lower()

        if action == 'f':
            break
        elif action == 'b':
            return calculate_money() # Restart the process
        
        try:
            percent = float(action)
            reduction = current_amount * (percent / 100)
            new_amount = current_amount - reduction
            
            # Store for final display
            history.append(f"{current_amount} * {percent}% = {new_amount}")
            
            current_amount = new_amount
            print(f"Result: {current_amount}")
        except ValueError:
            print("Invalid input. Enter a number, 'b', or 'f'.")

    # Final Display
    print("\n--- Final Calculation ---")
    for step in history:
        print(step)
    print(f"Your Money is = {current_amount}")

if __name__ == "__main__":
    calculate_money()
