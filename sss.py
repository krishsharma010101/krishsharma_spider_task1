import random


PRIME = 2**127 - 1  

def _mod_inv(a, p=PRIME):
    
   
    def egcd(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x1, y1 = egcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

    g, x, _ = egcd(a, p)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % p

def _eval_poly(poly, x, p=PRIME):
   
    result = 0
    for i, coef in enumerate(poly):
        result = (result + (coef * pow(x, i, p))) % p
    return result

def split_secret(secret, n, k, p=PRIME):
    
    if not (1 <= k <= n):
        raise ValueError("Threshold k must be between 1 and n")

    
    poly = [secret] + [random.randint(0, p-1) for _ in range(k-1)]

    shares = []
    for x in range(1, n+1):
        y = _eval_poly(poly, x, p)
        shares.append((x, y))
    return shares

def lagrange_interpolate(x, x_s, y_s, p=PRIME):
   
    total = 0
    k = len(x_s)
    for i in range(k):
        xi, yi = x_s[i], y_s[i]

        # Compute L_i(x)
        num, den = 1, 1
        for j in range(k):
            if j == i:
                continue
            xj = x_s[j]
            num = (num * (x - xj)) % p
            den = (den * (xi - xj)) % p

        inv_den = _mod_inv(den, p)
        term = yi * num * inv_den
        total = (total + term) % p
    return total

def reconstruct_secret(shares, k, p=PRIME):
   
    if len(shares) < k:
        raise ValueError("Not enough shares to reconstruct the secret")

    x_s, y_s = zip(*shares[:k])
    return lagrange_interpolate(0, x_s, y_s, p)


# === Demonstration ===
if __name__ == "__main__":
    secret = 12345678901234567890
    n = int(input())
    k = int(input())

    print(f"Original secret: {secret}")
    shares = split_secret(secret, n, k)
    print(f"Generated {n} shares (need any {k} to reconstruct):")
    for share in shares:
        print(f"Share {share[0]}: {share[1]}")

    # Pick any k shares for reconstruction
    selected_shares = random.sample(shares, k)
    print(f"\nSelected shares for reconstruction: {selected_shares}")

    recovered_secret = reconstruct_secret(selected_shares, k)
    print(f"Reconstructed secret: {recovered_secret}")

    assert secret == recovered_secret, "Reconstruction failed!"
