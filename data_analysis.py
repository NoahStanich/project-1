import pandas as pd

# Load the dataset
df = pd.read_csv("All_Diets.csv")

# Basic inspection
print("Dataset shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values per column:")
print(df.isnull().sum())

# STEP 2: Data Cleaning

# Standardize text columns
df['Diet_type'] = df['Diet_type'].str.strip().str.title()
df['Cuisine_type'] = df['Cuisine_type'].str.strip().str.title()

# Convert macronutrient columns to numeric (safety check)
macro_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
df[macro_cols] = df[macro_cols].apply(pd.to_numeric, errors='coerce')

# Fill missing numeric values with column mean
df[macro_cols] = df[macro_cols].fillna(df[macro_cols].mean())

# Verify cleaning
print("\nAfter cleaning - missing values:")
print(df.isnull().sum())

# STEP 3: Core Nutritional Analysis

# 1. Average macronutrient content per diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

print("\nAverage macronutrient content per diet type:")
print(avg_macros)

# 2. Top 5 protein-rich recipes per diet type
top_protein_recipes = (
    df.sort_values('Protein(g)', ascending=False)
      .groupby('Diet_type')
      .head(5)[['Diet_type', 'Recipe_name', 'Protein(g)', 'Cuisine_type']]
)

# Grouped output for readability
for diet, group in top_protein_recipes.groupby('Diet_type'):
    print(f"\nTop 5 protein-rich recipes for {diet}:")
    print(group[['Recipe_name', 'Protein(g)', 'Cuisine_type']])



# 3. Diet type with the highest average protein
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
highest_protein_value = avg_macros['Protein(g)'].max()

print(f"\nDiet type with highest average protein: {highest_protein_diet} "
      f"({highest_protein_value:.2f} g)")

# 4. Most common cuisine per diet type
common_cuisines = (
    df.groupby('Diet_type')['Cuisine_type']
      .agg(lambda x: x.value_counts().idxmax())
)

print("\nMost common cuisine per diet type:")
print(common_cuisines)

# STEP 4: Derived Nutritional Metrics

import numpy as np

# Avoid division by zero by replacing 0 with NaN
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)'].replace(0, np.nan)
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)'].replace(0, np.nan)

print("\nSample of derived nutritional ratios:")
print(df[['Recipe_name', 'Diet_type', 'Protein_to_Carbs_ratio', 'Carbs_to_Fat_ratio']].head())

# STEP 5: Visualizations

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# 1. Bar charts for average macronutrients
avg_macros.plot(kind='bar', figsize=(10, 6))
plt.title("Average Macronutrient Content by Diet Type")
plt.ylabel("Average grams")
plt.xlabel("Diet Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Heatmap for macronutrient relationships
plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Macronutrient Heatmap by Diet Type")
plt.tight_layout()
plt.show()

# 3. Scatter plot of top protein-rich recipes
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=top_protein_recipes,
    x="Cuisine_type",
    y="Protein(g)",
    hue="Diet_type",
    s=100
)
plt.title("Top 5 Protein-Rich Recipes by Cuisine")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


