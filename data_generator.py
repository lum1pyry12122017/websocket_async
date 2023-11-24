import pandas as pd
import random

# Luodaan tietojoukko
data = []

for i in range(851):
    sarake1 = (i // 3) * 3
    sarake2 = random.randint(-190, 190)
    sarake3 = random.randint(0, 100)
    sarake4 = float(sarake1) + random.random()
    sarake5 = 10 * (i + 1)
    sarake6 = random.uniform(-190, 190)

    data.append([sarake1, sarake2, sarake3, sarake4, sarake5, sarake6])

# Luodaan DataFrame
df = pd.DataFrame(data, columns=['Sarake1', 'Sarake2', 'Sarake3', 'Sarake4', 'Sarake5', 'Sarake6'])

df.head()  # Näytetään ensimmäiset rivit esimerkkinä

df.to_csv("1xxxx.csv")