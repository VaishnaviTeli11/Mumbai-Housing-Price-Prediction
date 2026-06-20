import pandas as pd
df= pd.read_csv("data/raw/mumbai_housing_prices.csv")
print("Shape of Dataset:", df.shape)
print(df.head())
print("Columns: ", df.columns.tolist())
print(df.isnull().sum())
print(df.describe())
print(df.dtypes)
print(df['Area'].unique())

from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(drop='first', sparse_output=False)

encoded = encoder.fit_transform(df[['Area']]).astype(int)

encoded_df = pd.DataFrame(
    encoded,
    columns=encoder.get_feature_names_out(['Area']),
    index=df.index
)

df = pd.concat([df.drop('Area', axis=1), encoded_df], axis=1)

print(df)
print("Columns: ", df.columns.tolist())

df.to_csv("data/cleaned/mumbai_housing_price_cleaned.csv", index=False)