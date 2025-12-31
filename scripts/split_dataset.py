import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('data/dataset_800.csv', sep=';', decimal=',')

print(f"Total data: {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")

# Pisahkan features (X) dan target (y)
X = df.drop('Yield_tons_per_hectare', axis=1)
y = df['Yield_tons_per_hectare']

# Split 80:20 dengan random_state untuk reproducibility
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42
)

print(f"\nTraining set: {len(X_train)} rows ({len(X_train)/len(df)*100:.1f}%)")
print(f"Testing set: {len(X_test)} rows ({len(X_test)/len(df)*100:.1f}%)")

# Preprocessing: Convert boolean to int
X_train['Fertilizer_Used'] = X_train['Fertilizer_Used'].astype(int)
X_train['Irrigation_Used'] = X_train['Irrigation_Used'].astype(int)
X_test['Fertilizer_Used'] = X_test['Fertilizer_Used'].astype(int)
X_test['Irrigation_Used'] = X_test['Irrigation_Used'].astype(int)

# One-hot encode categorical columns in specific order to match training
X_train_encoded = pd.get_dummies(X_train, columns=['Crop'], drop_first=True)
X_train_encoded = pd.get_dummies(X_train_encoded, columns=['Soil_Type'], drop_first=True)
X_train_encoded = pd.get_dummies(X_train_encoded, columns=['Weather_Condition'], drop_first=True)

X_test_encoded = pd.get_dummies(X_test, columns=['Crop'], drop_first=True)
X_test_encoded = pd.get_dummies(X_test_encoded, columns=['Soil_Type'], drop_first=True)
X_test_encoded = pd.get_dummies(X_test_encoded, columns=['Weather_Condition'], drop_first=True)

# Align test data columns with train data
for col in X_train_encoded.columns:
    if col not in X_test_encoded.columns:
        X_test_encoded[col] = 0

for col in X_test_encoded.columns:
    if col not in X_train_encoded.columns:
        X_test_encoded.drop(col, axis=1, inplace=True)

# Expected column order from trained model
expected_columns = [
    'Rainfall_mm', 'Temperature_Celsius', 'Fertilizer_Used', 'Irrigation_Used', 'Days_to_Harvest',
    'Crop_Cotton', 'Crop_Maize', 'Crop_Rice', 'Crop_Soybean', 'Crop_Wheat',
    'Soil_Type_Clay', 'Soil_Type_Loam', 'Soil_Type_Peaty', 'Soil_Type_Sandy', 'Soil_Type_Silt',
    'Weather_Condition_Rainy', 'Weather_Condition_Sunny'
]

# Reorder columns to match model expectations
X_train_encoded = X_train_encoded[expected_columns]
X_test_encoded = X_test_encoded[expected_columns]

print(f"\nAfter encoding:")
print(f"Training features: {X_train_encoded.shape[1]} columns")
print(f"Testing features: {X_test_encoded.shape[1]} columns")

# Save ke CSV (dengan encoding sudah diterapkan)
X_train_encoded.to_csv('data/X_train.csv', index=False)
X_test_encoded.to_csv('data/X_test.csv', index=False)
y_train.to_csv('data/y_train.csv', index=False, header=True)
y_test.to_csv('data/y_test.csv', index=False, header=True)

print("\n✓ Dataset berhasil dibagi dan disimpan (one-hot encoded):")
print("  - data/X_train.csv (640 rows)")
print("  - data/X_test.csv (160 rows)")
print("  - data/y_train.csv (640 rows)")
print("  - data/y_test.csv (160 rows)")
