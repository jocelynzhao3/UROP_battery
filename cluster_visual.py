import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
membership_df = pd.read_csv('cluster_memberships.csv')

# Set the battery names as the index
membership_df.set_index('BatteryName', inplace=True)

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(membership_df[['Cluster_1', 'Cluster_2', 'Cluster_3']], cmap='viridis', annot=True, fmt='.2f', cbar_kws={'label': 'Membership Percentage'})
plt.title('Heatmap of Membership Percentages for Each Battery and Cluster')
plt.xlabel('Cluster')
plt.ylabel('Battery Name')
plt.xticks(ticks=range(3), labels=['Cluster_1', 'Cluster_2', 'Cluster_3'], rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

plt.show()
