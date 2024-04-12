## Foundry

**Foundry is a blazing fast, portable and modular toolkit for Ethereum application development written in Rust.**

Foundry consists of:

-   **Forge**: Ethereum testing framework (like Truffle, Hardhat and DappTools).
-   **Cast**: Swiss army knife for interacting with EVM smart contracts, sending transactions and getting chain data.
-   **Anvil**: Local Ethereum node, akin to Ganache, Hardhat Network.
-   **Chisel**: Fast, utilitarian, and verbose solidity REPL.

## Documentation

https://book.getfoundry.sh/

## Usage

### Build

```shell
$ forge build
```

### Test

```shell
$ forge test
```

### Format

```shell
$ forge fmt
```

### Gas Snapshots

```shell
$ forge snapshot
```

### Anvil

```shell
$ anvil
```

### Deploy

```shell
$ forge script script/Counter.s.sol:CounterScript --rpc-url <your_rpc_url> --private-key <your_private_key>
```

### Cast

```shell
$ cast <subcommand>
```

### Help

```shell
$ forge --help
$ anvil --help
$ cast --help
```

### 1. Profitable Path, amountIn, amountOut, and Final Reward

**Profitable Path:**
- Swap Path: Token A → Token B
- `amountIn`: 1,000,000 units of Token A (example figure)
- `amountOutMin`: 900,000 units of Token B (minimum expected, example figure)
- **Final Reward (Token B Balance):** The output from the swap, which should ideally be at least as much as `amountOutMin`, depending on market conditions and slippage.

### 2. Slippage in AMM and Uniswap V2's Approach

**Slippage** is the difference between the expected price of a transaction and the executed price, common in AMMs due to price fluctuations arising from trade size impacting supply and demand.

**Uniswap V2’s Solution:**
Uniswap V2 mitigates slippage using the **Constant Product Formula** \( x \times y = k \), ensuring the product of the reserves remains constant post-trade. Users specify an `amountOutMin` to protect against excessive slippage, ensuring they do not receive less than this threshold from trades.

### 3. Rationale Behind Minimum Liquidity Subtraction in UniswapV2Pair's `mint` Function

**Minimum Liquidity Mechanism:**
Upon the initial provision of liquidity, Uniswap subtracts a fixed amount of 1000 liquidity tokens and permanently locks them. This process is intended to prevent manipulation of the AMMs by avoiding divisions by zero and ensuring the k (constant product) starts from a small, but nonzero, value.

### 4. Liquidity Calculation Formula in Subsequent Deposits

**Purpose of Specific Formula:**
For subsequent liquidity deposits (after the initial setup), liquidity tokens are minted based on the formula:
\[ \text{liquidity} = \min\left(\frac{\text{amountA} \times \text{totalLiquidity}}{\text{reserveA}}, \frac{\text{amountB} \times \text{totalLiquidity}}{\text{reserveB}}\right) \]
This formula ensures that the share of new liquidity tokens minted corresponds proportionally to the smallest possible increase in reserves relative to the existing total liquidity. It maintains a balanced value contribution from each token type, safeguarding the pool's integrity and value distribution.

### 5. Sandwich Attacks and Their Impact

**Sandwich Attack Explanation:**
A sandwich attack is a type of manipulation where a trader spots a pending transaction on an AMM like Uniswap that will impact the price of a token, and places one order ahead of it and one directly after it. The attacker benefits from the price slippage induced by the initial large transaction.

**Impact on Users:**
- The user’s transaction might execute at a worse rate than expected due to the manipulated prices.
- The attacker profits from the price movement, which can mean significant extra costs for regular users if the initial transaction was large.
