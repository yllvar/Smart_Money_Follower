### Smart Money Follower
___

#### Overview
The **Smart Money Follower** is a Python-based tool designed to analyze and follow top-performing wallets in the cryptocurrency space using the GMGN.ai API. It provides insights into wallet activities, evaluates traded tokens, and presents data in a structured format for analysis.

<img width="584" alt="Screenshot 2025-02-01 at 15 46 44" src="https://github.com/user-attachments/assets/728135f5-10d9-4ccf-9e2a-955638f9b73f" />

#### Features
- **Fetching Top Wallets**: Utilizes the GMGN.ai API to fetch top performing wallets based on specified criteria (`timeframe` and `walletTag`).
- **Analyzing Wallet Activity**: Analyzes trading activities of identified wallets over a period (`period`).
- **Evaluating Tokens**: Retrieves detailed information and USD prices of tokens traded by analyzed wallets.
- **Output Presentation**: Presents analyzed data in a tabulated format, facilitating easy interpretation and decision-making.


#### Example Output
```
+------+-------------------------------------+--------------------------+----------------+----------------+---------------------+
| Rank |           Wallet Address            | Realized Profit (SOL or USD) | Buy Transactions | Sell Transactions |     Last Active     |
+------+-------------------------------------+--------------------------+----------------+----------------+---------------------+
|  1   |     0x5f04c1a42770f23ed69a1b5a8dd04c7 |           12.34           |       56       |       32       | 2024-07-16 12:34:56 |
|  2   |     0x2c0d80f1b09829c70b7a0c0d5b69d1e |            9.87           |       40       |       25       | 2024-07-16 10:20:15 |
|  3   |     0x1a3e47f5c9234fe7d71c54efb65f94e |           -5.67           |       22       |       15       | 2024-07-15 09:45:30 |
+------+-------------------------------------+--------------------------+----------------+----------------+---------------------+
Note: The 'Realized Profit' is represented in SOL.
```

#### Notes
- Adjust rate limits (`time.sleep(1)`) according to API usage guidelines to prevent rate limiting issues.
- Logging is implemented to track errors and activities for debugging purposes.

#### This code is based on https://github.com/1f1n repository: https://github.com/1f1n/gmgnai-wrapper

Shout out to 1f1n
___

In order to use this, code, you need to:
1. clone this repo
2. install dependencies pip install -r requirements.txt
3. run python wallet.py or python smartMoney.py

# Feel free to use and modify
