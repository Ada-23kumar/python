from collections import defaultdict

# Function to compute FIRST sets
def compute_first(grammar):
    first = defaultdict(set)
    
    def first_of(symbol):
        if symbol in first:
            return first[symbol]
        
        # If the symbol is a terminal or ε, its FIRST set is itself
        if symbol not in grammar:
            return {symbol}
        
        # For non-terminals, compute FIRST based on productions
        for production in grammar[symbol]:
            for sym in production:
                if sym == 'ε':
                    first[symbol].add('ε')
                    break
                first_sym = first_of(sym)
                first[symbol].update(first_sym - {'ε'})
                if 'ε' not in first_sym:
                    break
            else:
                first[symbol].add('ε')
        return first[symbol]
    
    # Compute FIRST for all non-terminals
    for non_terminal in grammar:
        first_of(non_terminal)
    
    return first

# Function to compute FOLLOW sets
def compute_follow(grammar, first):
    follow = defaultdict(set)
    start_symbol = next(iter(grammar))  # First non-terminal is the start symbol
    follow[start_symbol].add('$')  # Add $ to the FOLLOW of the start symbol
    
    while True:
        updated = False
        follow_old = {k: v.copy() for k, v in follow.items()}
        
        for non_terminal in grammar:
            for production in grammar[non_terminal]:
                for i, symbol in enumerate(production):
                    if symbol in grammar:  # Only process non-terminals
                        # Add FIRST of the next symbol to FOLLOW of current symbol
                        next_symbols = production[i+1:]
                        if next_symbols:
                            first_next = set()
                            for sym in next_symbols:
                                first_next.update(first[sym] - {'ε'})
                                if 'ε' not in first[sym]:
                                    break
                            else:
                                first_next.add('ε')
                            
                            # If ε is in FIRST of the next symbols, add FOLLOW of the non-terminal
                            if 'ε' in first_next:
                                follow[symbol].update(follow[non_terminal])
                            follow[symbol].update(first_next - {'ε'})
                        else:
                            # If no next symbols, add FOLLOW of the non-terminal
                            follow[symbol].update(follow[non_terminal])
                        
                        # Check if FOLLOW set was updated
                        if follow[symbol] - follow_old.get(symbol, set()):
                            updated = True
        
        # If no updates were made in this iteration, stop
        if not updated:
            break
    
    return follow

# Function to input grammar from the user
def input_grammar():
    grammar = defaultdict(list)
    print("Enter the grammar productions (one per line). Use '->' for productions and '|' for alternatives.")
    print("Example: E -> T E' | ε")
    print("Enter 'done' when finished.")
    
    while True:
        production = input("> ").strip()
        if production.lower() == 'done':
            break
        if '->' not in production:
            print("Invalid production. Use '->' to separate non-terminal and productions.")
            continue
        
        non_terminal, productions = production.split('->')
        non_terminal = non_terminal.strip()
        productions = [p.strip().split() for p in productions.split('|')]
        grammar[non_terminal].extend(productions)
    
    return grammar

# Main function
def main():
    # Input grammar from the user
    grammar = input_grammar()
    
    # Compute FIRST and FOLLOW sets
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    
    # Print FIRST sets
    print("\nFIRST Sets:")
    for non_terminal, first_set in first.items():
        print(f"FIRST({non_terminal}) = {first_set}")
    
    # Print FOLLOW sets
    print("\nFOLLOW Sets:")
    for non_terminal, follow_set in follow.items():
        print(f"FOLLOW({non_terminal}) = {follow_set}")

# Run the program
if __name__ == "__main__":
    main()