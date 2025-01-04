### Smart Money Follower

Smart Money Follower OG Developer: https://github.com/yllvar <br>
OG Repo: https://github.com/yllvar/Smart_Money_Follower <br><br>
GMGN.ai API Wrapper OG Developer: https://github.com/1f1n <br>
OG Repo: https://github.com/1f1n/gmgnai-wrapper

#### Overview
The **Smart Money Follower** is a Python-based tool designed to analyze and follow top-performing wallets in the cryptocurrency space using the GMGN.ai API. It provides insights into wallet activities, evaluates traded tokens, and presents data in a structured format for analysis.

#### Features
- **Fetching Top Wallets**: Utilizes the GMGN.ai API to fetch top performing wallets based on specified criteria (`timeframe` and `walletTag`).
- **Analyzing Wallet Activity**: Analyzes trading activities of identified wallets over a period (`period`).
- **Evaluating Tokens**: Retrieves detailed information and USD prices of tokens traded by analyzed wallets.
- **Output Presentation**: Presents analyzed data in a tabulated format, facilitating easy interpretation and decision-making.

#### Requirements
- Python 3.7+
- Dependencies:
  - `fake-useragent`
  - `tabulate`
  - `tls_client`

## Setup
#### 1. **Clone Git**
   
   ```
   git clone https://github.com/LetsStartWithPurple/Smart_Money_Follower.git
   ```
#### 2. **Start Virtual Environment**

Navigate to the project directory:
  ```bash
  cd Smart_Money_Follower
  ```
Create Venv
  ```bash
  python3 -m venv venv
  ```
Start Virtual Environment
  ```bash
  source venv/bin/activate
  ```

#### 4. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

#### 5. **Execution**:
   ```bash
   python smart_money_follower.py
   ```

#### Usage
- Upon execution, the script fetches top wallets, analyzes their recent activities, evaluates tokens they've traded, and prints out a summarized analysis including realized profits, transaction volumes, and last activity timestamps.

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
