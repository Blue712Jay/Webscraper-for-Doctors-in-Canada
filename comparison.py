import pandas as pd



# Load both CSV files
df1 = pd.read_csv("kijijitest7.csv")
df2 = pd.read_csv("kijijitest8.csv")

# Get the values in column "C" as sets (ignoring NaNs)
values1 = set(df1["Ad ID Number"].dropna())
values2 = set(df2["Ad ID Number"].dropna())

# Find common values
common_values = values1.intersection(values2)

# Output
if common_values:
    print(common_values)  # You can convert to list if needed
else:
    print("None")



print(len(common_values))