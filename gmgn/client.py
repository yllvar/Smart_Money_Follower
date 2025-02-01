import random
import tls_client
from fake_useragent import UserAgent

# author - 1f1n
# date - 05/06/2024

class gmgn:
    BASE_URL = "https://gmgn.ai/defi/quotation"

    def __init__(self):
        pass

    def randomiseRequest(self):
        self.identifier = random.choice([browser for browser in tls_client.settings.ClientIdentifiers.__args__ if browser.startswith(('chrome', 'safari', 'firefox', 'opera'))])
        self.sendRequest = tls_client.Session(random_tls_extension_order=True, client_identifier=self.identifier)

        parts = self.identifier.split('_')
        identifier, version, *rest = parts
        other = rest[0] if rest else None

        os = 'windows'
        if identifier == 'opera':
            identifier = 'chrome'
        elif version == 'ios':
            os = 'ios'
        else:
            os = 'windows'

        self.user_agent = UserAgent(browsers=[identifier], os=[os]).random

        self.headers = {
            'Host': 'gmgn.ai',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'dnt': '1',
            'priority': 'u=1, i',
            'referer': 'https://gmgn.ai/?chain=sol',
            'user-agent': self.user_agent
        }
        

    def getTokenInfo(self, contractAddress: str) -> dict:
        """
        Gets info on a token.
        """
        self.randomiseRequest()
        if not contractAddress:
            return "You must input a contract address."
        url = f"{self.BASE_URL}/v1/tokens/sol/{contractAddress}"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()

        return jsonResponse
    
    def getNewPairs(self, limit: int = None) -> dict:
        """
        Limit - Limits how many tokens are in the response.
        """
        self.randomiseRequest()
        if not limit:
            limit = 50
        elif limit > 50:
            return "You cannot have more than check more than 50 pairs."
        
        url = f"{self.BASE_URL}/v1/pairs/sol/new_pairs?limit={limit}&orderby=open_timestamp&direction=desc&filters[]=not_honeypot"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse
    
    def getTrendingWallets(self, timeframe: str = None, walletTag: str = None) -> dict:
        """
        Gets a list of trending wallets based on a timeframe and a wallet tag.

        Timeframes\n
        1d = 1 Day\n
        7d = 7 Days\n
        30d = 30 days\n

        ----------------

        Wallet Tags\n
        pump_smart = Pump.Fun Smart Money\n
        smart_degen = Smart Money\n
        reowned = KOL/VC/Influencer\n
        snipe_bot = Snipe Bot\n

        """
        self.randomiseRequest()
        if not timeframe:
            timeframe = "7d"
        if not walletTag:
            walletTag = "smart_degen"
        
        url = f"{self.BASE_URL}/v1/rank/sol/wallets/{timeframe}?tag={walletTag}&orderby=pnl_{timeframe}&direction=desc"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse
    
    def getTrendingTokens(self, timeframe: str = None) -> dict:
        """
        Gets a list of trending tokens based on a timeframe.

        Timeframes\n
        1m = 1 Minute\n
        5m = 5 Minutes\n
        1h = 1 Hour\n
        6h = 6 Hours\n
        24h = 24 Hours\n
        """
        timeframes = ["1m", "5m", "1h", "6h", "24h"]
        self.randomiseRequest()
        if timeframe not in timeframes:
            return "Not a valid timeframe."

        if not timeframe:
            timeframe = "1h"

        if timeframe == "1m":
            url = f"{self.BASE_URL}/v1/rank/sol/swaps/{timeframe}?orderby=swaps&direction=desc&limit=20"
        else:
            url = f"{self.BASE_URL}/v1/rank/sol/swaps/{timeframe}?orderby=swaps&direction=desc"
        
        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse

    def getTokensByCompletion(self, limit: int = None) -> dict:
        """
        Gets tokens by their bonding curve completion progress.\n

        Limit - Limits how many tokens in the response.
        """
        self.randomiseRequest()
        if not limit:
            limit = 50
        elif limit > 50:
            return "Limit cannot be above 50."

        url = f"{self.BASE_URL}/v1/rank/sol/pump?limit={limit}&orderby=progress&direction=desc&pump=true"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse
    
    def findSnipedTokens(self, size: int = None) -> dict:
        """
        Gets a list of tokens that have been sniped.\n

        Size - The amount of tokens in the response
        """
        self.randomiseRequest()
        if not size:
            size = 10
        elif size > 39:
            return "Size cannot be more than 39"
        
        url = f"{self.BASE_URL}/v1/signals/sol/snipe_new?size={size}&is_show_alert=false&featured=false"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse

    def getGasFee(self):
        """
        Get the current gas fee price.
        """
        self.randomiseRequest()
        url = f"{self.BASE_URL}/v1/chains/sol/gas_price"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse
    
    def getTokenUsdPrice(self, contractAddress: str = None) -> dict:
        """
        Get the realtime USD price of the token.
        """
        self.randomiseRequest()
        if not contractAddress:
            return "You must input a contract address."
        
        url = f"{self.BASE_URL}/v1/sol/tokens/realtime_token_price?address={contractAddress}"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse

    def getTopBuyers(self, contractAddress: str = None) -> dict:
        """
        Get the top buyers of a token.
        """
        self.randomiseRequest()
        if not contractAddress:
            return "You must input a contract address."
        
        url = f"{self.BASE_URL}/v1/tokens/top_buyers/sol/{contractAddress}"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse

    def getSecurityInfo(self, contractAddress: str = None) -> dict:
        """
        Gets security info about the token.
        """
        self.randomiseRequest()
        if not contractAddress:
            return "You must input a contract address."
        
        url = f"{self.BASE_URL}/v1/tokens/security/sol/{contractAddress}"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse
    
    def getWalletInfo(self, walletAddress: str = None, period: str = None) -> dict:
        """
        Gets various information about a wallet address.

        Period - 7d, 30d - The timeframe of the wallet you're checking.
        """
        self.randomiseRequest()
        periods = ["7d", "30d"]

        if not walletAddress:
            return "You must input a wallet address."
        if not period or period not in periods:
            period = "7d"
        
        url = f"{self.BASE_URL}/v1/smartmoney/sol/walletNew/{walletAddress}?period={period}"

        request = self.sendRequest.get(url, headers=self.headers)

        jsonResponse = request.json()['data']

        return jsonResponse
