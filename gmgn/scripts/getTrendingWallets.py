from ..client import gmgn

gmgn = gmgn()

getTrendingWallets = gmgn.getTrendingWallets(timeframe="7d", walletTag="smart_degen")

print(getTrendingWallets)