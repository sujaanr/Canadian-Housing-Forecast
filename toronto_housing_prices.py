import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point, Polygon
from scipy.stats import norm, probplot, stats
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
import warnings
warnings.filterwarnings('ignore')

# Constants
DATA_DIR = '/kaggle/input/torontohousingprices'
PLOT_SIZE = (10, 8)

# Load Data
def load_data(file_path):
    try:
        return pd.read_csv(os.path.join(DATA_DIR, file_path))
    except FileNotFoundError:
        print("File not found.")
        return None

# Display all files in the directory
def display_files():
    for dirname, _, filenames in os.walk(DATA_DIR):
        for filename in filenames:
            print(os.path.join(dirname, filename))

# Display directory structure
display_files()

# Load dataset
df_train = load_data('dataset_final.csv')
df_train.columns = [col.strip().lower().replace(' ', '_') for col in df_train.columns]

# Analyze 'sold_price'
df_train['sold_price'].describe()

# Sold Price histogram
sns.distplot(df_train['sold_price'], fit=norm)
plt.title('Sold Price Distribution')
plt.show()

# Scatter plot 'square_footage'/'sold_price'
sns.scatterplot(x='square_footage', y='sold_price', data=df_train)
plt.title('Price vs Square Footage')
plt.show()

# Heat Map of House Prices by Neighbourhood in Toronto
def plot_heat_map():
    # Load shape file for mapping
    neighbourhood_map = gpd.read_file('../input/folder/forAnalysis/Neighbourhoods/Neighbourhoods.shp')
    neighbourhood_map['neighbourhood'] = neighbourhood_map['FIELD_7'].str.replace(' \(.+\)', '').str.lower()

    # Prepare data for merging
    community_prices = df_train.groupby('community')['sold_price'].mean().reset_index()
    community_prices.columns = ['neighbourhood', 'avg_price']

    # Merge and plot
    merged = neighbourhood_map.set_index('neighbourhood').join(community_prices.set_index('neighbourhood'))
    fig, ax = plt.subplots(1, figsize=(15, 10))
    merged.plot(column='avg_price', cmap='coolwarm', linewidth=0.8, ax=ax, edgecolor='0.8')
    ax.axis('off')
    plt.show()

plot_heat_map()

# Correlation matrix
corr_matrix = df_train.corr()
sns.heatmap(corr_matrix, vmax=.8, square=True)
plt.show()

# Begin Data Engineering
# Encoding categorical data
def encode_features(df, cols):
    encoder = OneHotEncoder(handle_unknown='ignore')
    for col in cols:
        df = pd.get_dummies(df, columns=[col], prefix=[col], drop_first=True)
    return df

df_train = encode_features(df_train, ['type', 'style', 'community'])

# Normalize skewed data
def normalize_data(df, column):
    df[f'log_{column}'] = np.log(df[column])
    sns.distplot(df[f'log_{column}'], fit=norm)
    plt.show()

normalize_data(df_train, 'square_footage')

# Model Building
def build_model(input_shape):
    model = Sequential()
    model.add(Dense(50, activation='relu', input_dim=input_shape))
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train-test split
X = df_train.drop('sold_price', axis=1)
y = df_train['sold_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the model
model = build_model(X_train.shape[1])
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=2)

# Visualize training history
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()

# Save and load the model
model.save('model.h5')
loaded_model = load_model('model.h5')

# Make predictions
predictions = loaded_model.predict(X_test)
print(predictions[:5])  # Display first 5 predictions



