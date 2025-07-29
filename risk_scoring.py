import random
import csv

with open("wallets.txt", "r") as f:
    wallets = [line.strip() for line in f if line.strip()]

def generate_fake_features():
    """Simulate fake deposit/borrow/liquidation stats like real Compound data"""
    deposits = random.uniform(100, 10000)
    borrows = random.uniform(0, 12000)
    repays = borrows * random.uniform(0.3, 1.2)  # sometimes repays less, sometimes more
    liquidations = random.randint(0, 3) if borrows > deposits else 0
    return deposits, borrows, repays, liquidations

def calculate_score(deposits, borrows, repays, liquidations):
    """Risk scoring logic based on simple ratios"""
    score = 500  
    repay_ratio = repays / borrows if borrows > 0 else 1
    liquidation_ratio = liquidations / (borrows / 1000 + 1)  # normalized

    if repay_ratio > 0.8:
        score += 200
    if liquidations == 0:
        score += 150
    if deposits > borrows:
        score += 50

    if liquidation_ratio > 0.3:
        score -= 200
    if borrows > deposits * 2:
        score -= 100

    return max(0, min(1000, int(score)))

results = []
for wallet in wallets:
    deposits, borrows, repays, liquidations = generate_fake_features()
    score = calculate_score(deposits, borrows, repays, liquidations)
    results.append((wallet, score))

# 3. Save to CSV
with open("wallet_scores.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["wallet_id", "score"])
    writer.writerows(results)

print("wallet_scores.csv generated with", len(results), "wallets!")
