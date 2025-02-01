import json
import logging
from datetime import datetime
from typing import List, Dict
from tabulate import tabulate
from gmgn import gmgn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wallet_analysis.log'),
        logging.StreamHandler()
    ]
)

# Suppress fake_useragent warnings
logging.getLogger('fake_useragent').setLevel(logging.ERROR)

class WalletAnalyzer:
    def __init__(self):
        self.gmgn = gmgn()
        self.logger = logging.getLogger("WalletAnalyzer")

    def safe_get(self, data: Dict, *keys, default=0):
        """Safely get nested dictionary values."""
        try:
            result = data
            for key in keys:
                result = result.get(key, default)
                if result is None:
                    return default
            return result
        except Exception:
            return default

    def get_trending_wallets(self, timeframe: str = "1d", wallet_tag: str = "smart_degen") -> List[Dict]:
        """Fetch and filter active trending wallets."""
        try:
            self.logger.info(f"Fetching trending wallets for {timeframe} timeframe with tag {wallet_tag}")
            response = self.gmgn.getTrendingWallets(timeframe=timeframe, walletTag=wallet_tag)

            if not response or 'rank' not in response:
                return []

            # Filter and format active wallets
            active_wallets = []
            current_time = datetime.now().timestamp()

            for wallet in response.get('rank', []):
                try:
                    # Get values with safe defaults
                    last_active = self.safe_get(wallet, 'last_active', default=0)
                    buy_count = self.safe_get(wallet, 'buy', default=0)
                    sell_count = self.safe_get(wallet, 'sell', default=0)
                    winrate = self.safe_get(wallet, 'winrate_7d', default=0)
                    realized_profit = self.safe_get(wallet, 'realized_profit', default=0)

                    # Skip inactive wallets
                    if current_time - last_active > 7 * 24 * 3600:
                        continue

                    # Skip wallets with no trades
                    if not buy_count and not sell_count:
                        continue

                    formatted_wallet = {
                        'wallet_address': self.safe_get(wallet, 'wallet_address', default='N/A'),
                        'realized_profit': round(float(realized_profit), 2),
                        'win_rate': round(float(winrate) * 100, 1) if winrate is not None else 0.0,
                        'trades': {
                            'buy': int(buy_count),
                            'sell': int(sell_count)
                        },
                        'last_active': datetime.fromtimestamp(last_active).strftime('%Y-%m-%d %H:%M'),
                        'risk_metrics': {
                            'honeypot_ratio': round(self.safe_get(wallet, 'risk', 'token_honeypot_ratio', default=0) * 100, 1),
                            'fast_tx_ratio': round(self.safe_get(wallet, 'risk', 'fast_tx_ratio', default=0) * 100, 1)
                        }
                    }
                    active_wallets.append(formatted_wallet)
                except Exception as e:
                    self.logger.warning(f"Error processing wallet: {e}")
                    continue

            # Sort by realized profit
            return sorted(active_wallets, key=lambda x: x['realized_profit'], reverse=True)

        except Exception as e:
            self.logger.error(f"Error fetching trending wallets: {e}")
            return []

    def display_wallet_analysis(self, wallets: List[Dict]) -> None:
        """Display wallet analysis in a formatted table."""
        if not wallets:
            self.logger.warning("No wallet data to display")
            return

        # Prepare table data
        headers = [
            "Index",
            "Wallet Address",
            "Profit (SOL)",
            "Win Rate",
            "Trades (B/S)",
            "Last Active",
            "Risk Metrics"
        ]

        table_data = []
        for idx, wallet in enumerate(wallets, start=1):
            try:
                # Format profit with commas
                profit = f"{wallet['realized_profit']:,.2f}"

                # Format win rate
                win_rate = f"{wallet['win_rate']}%"

                # Format trades
                trades = f"{wallet['trades']['buy']}/{wallet['trades']['sell']}"

                # Format risk metrics
                risk = f"HP:{wallet['risk_metrics']['honeypot_ratio']}% FT:{wallet['risk_metrics']['fast_tx_ratio']}%"

                table_data.append([
                    idx,
                    wallet['wallet_address'],  # Full wallet address for easy copying
                    profit,
                    win_rate,
                    trades,
                    wallet['last_active'],
                    risk
                ])
            except Exception as e:
                self.logger.warning(f"Error formatting wallet data: {e}")
                continue

        if not table_data:
            self.logger.warning("No valid wallet data to display")
            return

        # Print summary
        print(f"\n=== Smart Money Wallet Analysis ({len(table_data)} Active Wallets) ===")
        print(tabulate(table_data, headers=headers, tablefmt="grid", numalign="right"))

        try:
            # Print statistics
            total_profit = sum(w['realized_profit'] for w in wallets)
            avg_win_rate = sum(w['win_rate'] for w in wallets) / len(wallets) if wallets else 0
            print(f"\nSummary:")
            print(f"Total Profit: {total_profit:,.2f} SOL")
            print(f"Average Win Rate: {avg_win_rate:.1f}%")

            # Export to JSON
            self.export_to_json(wallets)
        except Exception as e:
            self.logger.error(f"Error calculating statistics: {e}")

    def export_to_json(self, data: List[Dict]) -> None:
        """Export analysis results to JSON file."""
        try:
            filename = 'wallet_analysis.json'
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Analysis exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {e}")

def main():
    try:
        analyzer = WalletAnalyzer()
        wallets = analyzer.get_trending_wallets()
        analyzer.display_wallet_analysis(wallets)
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
