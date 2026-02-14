import pandas as pd

# List of CSV input files (add as many as you want)
input_files = [
    "links.csv",
    "links2.csv",
    "links3.csv",
    "links4.csv",
    # "file5.csv",
]

output_file = "links_combined.csv"

columntitle = "url"

# ---- Merge without duplicates ----
combined_df = pd.DataFrame()
seen_ids = set()

for file in input_files:
    df = pd.read_csv(file)
    # Keep only rows with new Ad IDs
    df_unique = df[~df[columntitle].isin(seen_ids)]
    # Add these IDs to the seen set
    seen_ids.update(df_unique[columntitle].dropna())
    # Append to combined dataframe
    combined_df = pd.concat([combined_df, df_unique], ignore_index=True)

# Save result
combined_df.to_csv(output_file, index=False)

print(f"Merged CSV saved as {output_file} without duplicate Ad IDs.")