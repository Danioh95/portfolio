import pandas as pd
import matplotlib.pyplot as plt
from dict_xpaths import paths

df = pd.read_csv('my_data.csv')

# remove blank space in location
df['location'] = df['location'].str.lstrip()

# I remove  the tag related to batches, as they are not information that I will use
index_values = list(paths.keys())

mask = df['tag'].isin(index_values)
df_f = df[~mask]

# filter the dataframe to only include acquired startups
df_acquired = df_f[df_f['status'] == 'acquired']

# count the occurrences of each tag
tag_counts_acquired = df_acquired['tag'].value_counts().sort_values(ascending=False)[:10]

# plot the tag counts in a bar chart
plt.bar(tag_counts_acquired.index, tag_counts_acquired.values)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Tags')
plt.ylabel('Number of Acquired Startups')
plt.title('Top 10 Tags for Acquired Y Combinator Startups')


# 2-nd hypotesis

counts = df_f.groupby(['location', 'status']).size().unstack().fillna(0)
counts = counts.sort_values(by='active', ascending=False).head(10)

ax = counts.plot(kind='bar', stacked=True, figsize=(10, 6))

# Set the chart title and axis labels
ax.set_title('Top 10 Company Locations by Status')
ax.set_xlabel('Location')
ax.set_ylabel('Count')

# Add a legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])

plt.savefig('my_plot2.png', dpi=300, bbox_inches="tight")
plt.show()

