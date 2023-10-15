import streamlit as st
import pandas as pd
import re
import plotly.express as px

# Load your data
def load_data():
    df = pd.read_csv('Egyptian_Doctors_Data.csv') 
    return df

df = load_data()
if 'rate_count' in df.columns:
    # Create the 'number_of_visitors' column by converting 'rate_count' to string
    df['number_of_visitors'] = df['rate_count'].astype(str)
else:
    st.error("The 'rate_count' column does not exist in the DataFrame.")
#########################################

# Page Title
st.title("Egyptian Doctors Data Analysis")
# Small paragraph
st.write("This is the whole data with all the details for the Egyptian doctors covering various locations.")
# Display the raw data
st.subheader("Raw Data")
st.write(df)

# df['column_name'] = pd.to_numeric(df['column_name'], errors='coerce')


####################################################

#####

selected_specializations = st.multiselect('Select Specializations', df['specialization'].unique())
# Filter the DataFrame based on selected specializations
filtered_df = df[df['specialization'].isin(selected_specializations)]

# Create the scatter plot with the filtered data
fig2 = px.scatter(filtered_df, x='specialization', y='fees', title='Specialization vs. Appointment Fees')
# Display the plot using st.plotly_chart
st.plotly_chart(fig2)

# Create a scatter plot for specialization vs. fees
# fig2 = px.scatter(df, x='specialization', y='fees', title='Specialization vs. Appointment Fees')
# st.plotly_chart(fig2)

# Group the data by 'specialization' and calculate the average fees for each specialization
specialization_fees = df.groupby('specialization')['fees'].mean().reset_index()

# Sort the specializations by average fees in descending order
sorted_specializations_fees = specialization_fees.sort_values(by='fees', ascending=False)

# Select the top 10 specializations with the highest fees (highest to lowest)
top_10_specializations_fees = sorted_specializations_fees.head(10)

# Create a bar plot to visualize the relationship between specialization and fees
fig3 = px.bar(top_10_specializations_fees, x='specialization', y='fees',
              title='Top 10 Specializations with Highest Fees (Highest to Lowest)')

# Display the plot using st.plotly_chart
st.plotly_chart(fig3)

# Customize the chart (optional)
fig3.update_xaxes(title_text='Specialization')
fig3.update_yaxes(title_text='Average Fees')

# Rotate x-axis labels for better readability (optional)
fig3.update_layout(xaxis_tickangle=-45)

# Display the plot
st.plotly_chart(fig3)

# Group the data by 'clinic_location' and count the number of doctors in each governorate
governorate_counts = df['clinic_location'].value_counts().reset_index()
governorate_counts.columns = ['Governorate', 'Doctor Count']

# Display the result
st.subheader("Governorates with Most Doctors")
st.write(governorate_counts)

# Sort the governorates by doctor count in descending order and select the top 5
top_5_governorates = governorate_counts.head(5)

# Create a pie chart for the top 5 governorates
fig4 = px.pie(top_5_governorates, names='Governorate', values='Doctor Count', title='Top 5 Governorates with Most Doctors')

# Display the plot
st.plotly_chart(fig4)



import re
# Define a function to extract numbers from a string
def extract_numbers(text):
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0])
    else:
        return 0  # Return 0 if no numbers are found
df['number_of_visitors'] = df['rate_count'].astype(str)

# Apply the extract_numbers function to the 'number_of_visitors' column
df['number_of_visitors'] = df['number_of_visitors'].apply(extract_numbers)

# Group the data by doctor's name or identifier and calculate the total number of visitors
doctor_visitors = df.groupby('web_scraper_order')['number_of_visitors'].sum().reset_index()

# Sort the doctors by visitor count in descending order and select the top 10
top_10_doctors = doctor_visitors.nlargest(10, 'number_of_visitors')

# Display the result
print(top_10_doctors)


# Group the data by 'specialization' and calculate the total number of visitors for each specialization
specialization_visitors = df.groupby('specialization')['number_of_visitors'].sum().reset_index()

# Sort the specializations by total number of visitors in descending order
sorted_specializations_visitors = specialization_visitors.sort_values(by='number_of_visitors', ascending=False)

# Select the top 10 specializations with the highest number of visitors
top_10_specializations_visitors = sorted_specializations_visitors.head(10)

# Create a bar chart to visualize the number of visitors for the top 10 specializations
fig6 = px.bar(top_10_specializations_visitors, x='specialization', y='number_of_visitors',
               title='Top 10 Specializations with Highest Number of Visitors')

# Customize the chart (optional)
fig6.update_xaxes(title_text='Specialization')
fig6.update_yaxes(title_text='Number of Visitors')

# Rotate x-axis labels for better readability (optional)
fig6.update_layout(xaxis_tickangle=-45)

# Display the plot
st.plotly_chart(fig6)

# Group the data by 'specialization' and calculate the total number of visitors for each specialization
specialization_visitors = df.groupby('specialization')['number_of_visitors'].sum().reset_index()

# Sort the specializations by total number of visitors in descending order
sorted_specializations_visitors = specialization_visitors.sort_values(by='number_of_visitors', ascending=False)

# Select the top 10 specializations with the highest number of visitors
top_10_specializations_visitors = sorted_specializations_visitors.head(10)

# Create a treemap for the top 10 specializations with the highest number of visitors
fig7 = px.treemap(top_10_specializations_visitors, path=['specialization'], values='number_of_visitors',
                  title='Top 10 Specializations with Highest Number of Visitors (Treemap)')

# Display the plot
st.plotly_chart(fig7)

# Define waiting time categories
def categorize_waiting_time(waiting_time, threshold):
    if waiting_time <= threshold:
        return 'Short'
    elif threshold < waiting_time <= 2 * threshold:
        return 'Medium'
    else:
        return 'Long'

# Create a Streamlit slider to adjust the waiting time threshold
threshold = st.slider("Select Waiting Time Threshold", min_value=10, max_value=60, value=30, step=5)

# Categorize waiting times based on the selected threshold and create a new 'waiting_time_category' column
df['waiting_time_category'] = df['waiting_time'].apply(categorize_waiting_time, threshold=threshold)

# Group the data by 'specialization' and 'waiting_time_category' and calculate the count
specialization_waiting_time_counts = df.groupby(['specialization', 'waiting_time_category']).size().reset_index(name='count')

# Create a treemap for specialization vs. waiting time categories
fig8 = px.treemap(specialization_waiting_time_counts, path=['specialization', 'waiting_time_category'], values='count',
                  title='Specialization vs. Waiting Time Categories (Treemap)')

# Display the plot
st.plotly_chart(fig8)
