import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from fcmeans import FCM
import time

a = time.time()

# Load the data
df = pd.read_csv('cluster_data.csv')

# Extract battery names and features
battery_names = df.iloc[:, 0]  # First column: battery names
features = df.iloc[:, 1:]      # Remaining columns: battery features

# Check for missing values and handle them
if features.isnull().values.any():
    print("Missing values detected. Filling missing values with the mean of each column.")
    features.fillna(features.mean(), inplace=True)

# Preprocessing: Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Perform Fuzzy C-Means clustering
n_clusters = 3  # Adjust the number of clusters as needed
fcm = FCM(n_clusters=n_clusters)
fcm.fit(scaled_features)

# Get membership degrees
membership_degrees = fcm.u

# Determine the cluster with the highest membership degree for each battery
cluster_assignments = membership_degrees.argmax(axis=1) + 1  # Adding 1 to match 1-based cluster indexing

# Create a DataFrame with the results
# Membership degrees DataFrame
membership_df = pd.DataFrame(membership_degrees, columns=[f'Cluster_{i+1}' for i in range(n_clusters)])

# Add battery names to the DataFrame
membership_df.insert(0, 'BatteryName', battery_names)

# Add the assigned cluster column
membership_df['AssignedCluster'] = cluster_assignments

# Save the results to a new CSV file
membership_df.to_csv('cluster_memberships.csv', index=False)

b = time.time()
print("Clustering membership percentages saved to 'cluster_memberships.csv'")
print(f'Done in {b-a} seconds')  # ~0.02 seconds
