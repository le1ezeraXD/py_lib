import pandas as pd

#repeat line 2 in csv
df = pd.read_csv('/Users/device/Desktop/test.csv')

df_expanded = df.loc[df.index.repeat(2)].reset_index(drop=True)

df_expanded.to_csv('/Users/device/Desktop/test_expanded.csv', index=False)

print("over")