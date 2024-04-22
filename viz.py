import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd

#Data prep

#making a change (delete this)
df = pd.read_csv('Origin_usa.csv')

# Extract the year portion from the 'Year' column
df['year'] = df['year'].str.split('/').str[0]

df = df.dropna(subset=['year'])

# Convert the 'Year' column to integer type
df['year'] = df['year'].astype(int)

# Filter the DataFrame based on the year condition
filtered_df = df[df['year'].between(2007, 2022)]

grouped_df = filtered_df.groupby('year')['students'].sum()


filtered_df = filtered_df.drop(columns=['Unnamed: 5']).reset_index(drop=True)


# Streamlit app
st.title('Number of Students by Academic Type over Years')

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
grouped_df.plot(kind='bar', stacked=True, x='year', ax=ax)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.title('Number of Students by Academic Type over Years')
plt.legend(title='Academic Type')

# Display plot in Streamlit
st.pyplot(fig)


#'filtered_df' is our DataFrame containing student data with 'origin', 'students', and 'academic_type' columns

# Group the DataFrame by 'origin' and 'academic_type' and sum the 'students' column
origin_df = filtered_df.groupby(['origin', 'academic_type'])['students'].sum().reset_index()

# Create a Streamlit dropdown menu for selecting academic types
selected_academic_type = st.selectbox("Select Academic Type", origin_df['academic_type'].unique())

# Filter the DataFrame based on the selected academic type
filtered_origin_df = origin_df[origin_df['academic_type'] == selected_academic_type]

# Load a world shapefile or any other suitable geographical dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the origin DataFrame with the world dataset based on country names
world = world.merge(filtered_origin_df, left_on='name', right_on='origin', how='left')

# Fill NaN values with 0
world['students'] = world['students'].fillna(0)

# Plotting
fig, ax = plt.subplots(figsize=(15, 10))

# Plot the world map
world.boundary.plot(ax=ax)

# Plot countries with color representing the number of students
world.plot(column='students', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Add title and legend
plt.title(f'Number of Students by Origin for {selected_academic_type}')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Number of Students', loc='lower right')

# Display plot in Streamlit
st.pyplot(fig)

#pull request added
