from itertools import permutations, combinations, chain

# Initial liquidity data for token pairs.
liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def all_combinations(elements):
    """ Generate all possible combinations of the given list of elements. """
    all_combos = []
    for i in range(1, len(elements) + 1):
        for combo in combinations(elements, i):
            all_combos.append(combo)
    return all_combos

def all_paths(elements):
    """ Generate all possible paths through permutations of all combinations of elements. """
    results = []
    all_combos = all_combinations(elements)
    for combo in all_combos:
        permuted = permutations(combo)
        for item in permuted:
            results.append(item)
    return results

def swap(token_in, token_out, amount_in, liquidity):
    """ Perform a token swap calculation using constant product formula and update liquidity. """
    # Calculate amount considering the transaction fee
    amount_in_fee = amount_in * 0.997
    amount_out = 0

    # Determine the correct liquidity pair based on input and output tokens
    if (token_in, token_out) in liquidity:
        reserve_in, reserve_out = liquidity[(token_in, token_out)]
    elif (token_out, token_in) in liquidity:
        reserve_out, reserve_in = liquidity[(token_out, token_in)]
    else:
        # No liquidity pair found
        return 0

    # Constant product market maker formula
    k = reserve_in * reserve_out
    reserve_in_updated = reserve_in + amount_in_fee
    reserve_out_updated = k / reserve_in_updated
    amount_out = reserve_out - reserve_out_updated

    # Update the liquidity pool
    if (token_in, token_out) in liquidity:
        liquidity[(token_in, token_out)] = (reserve_in + amount_in, reserve_out_updated)
    else:
        liquidity[(token_out, token_in)] = (reserve_out_updated, reserve_in + amount_in)

    return amount_out

def find_best_route(liquidity, paths, initial_amount):
    """ Evaluate all paths to find the one yielding the highest amount of output tokens starting from a specific input amount. """
    best_output = 0
    best_path = ()
    for path in paths:
        liquidity_copy = dict(liquidity)
        full_path = ("tokenB",) + path + ("tokenB",)
        current_amount = initial_amount

        # Perform swaps along the path
        for i in range(len(full_path) - 1):
            token_in = full_path[i]
            token_out = full_path[i + 1]
            current_amount = swap(token_in, token_out, current_amount, liquidity_copy)

        # Check if the current path gives a better output
        if current_amount > best_output:
            best_output = current_amount
            best_path = path

    return best_output, best_path

# Calculate all possible paths excluding the base token "tokenB"
paths = all_paths(["tokenA", "tokenC", "tokenD", "tokenE"])

# Find the best path and output result for an initial amount of 5 units of "tokenB"
best_amount, best_path = find_best_route(liquidity, paths, 5)

# Format the best path for output
path_description = "tokenB->" + "->".join(best_path) + "->tokenB"
print(f'{path_description}, token balance={best_amount}')
