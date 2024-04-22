# PPHA 30537
# Spring 2024
# Homework 2 

# Attaullah Abbasi
# attaullahabbasi12

# Due date: Sunday April 21st before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.  Using functions for organization will be rewarded.

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.




# PART 1: Macro Data Exploration

# Question 1.1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.

import pandas as pd
import os

directory = '/Users/attaullah/Documents/homework-2-attaullahabbasi12'  
file_name = 'NST-EST2022-ALLDATA.csv'

# Creating the path
file_path = os.path.join(directory, file_name)

#loading it in dataframe 
population_data = pd.read_csv(file_path)

# checkin
print(population_data.head())

# Question 1.2: Your data only includes fips codes for states (STATE).  Use 
# the us library to crosswalk fips codes to state abbreviations.  Drop the
# fips codes.

import us

# Filtering the dataframe for rows with SUMLEV 40 (state-level data)
state_level_data = population_data[population_data['SUMLEV'] == 40].copy()

# treating state column as a string
state_level_data['STATE'] = state_level_data['STATE'].apply(lambda x: f'{x:02d}')

# Mapping FIPS code to state abbreviations
state_level_data['state_abbreviation'] = state_level_data['STATE'].map(us.states.mapping('fips', 'abbr'))

# Drop ping the original FIPS code
state_level_data.drop(columns=['STATE'], inplace=True)

# Printing to check 
print(state_level_data.head())

# Question 1.3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize for them.  Do not 
# create plots or use groupby; we will do that in future homeworks.  
# Show the relevant exploration output with print() statements.


# Printing the shape for size
print(f"The DataFrame has {state_level_data.shape[0]} rows and {state_level_data.shape[1]} columns.")

# short summary of the data frame
print("\nDataFrame Info:")
print(state_level_data.info())

# unique values in each column 
print("\nNumber of unique values per column:")
print(state_level_data.nunique())

#the central tendency, dispersion
print("\nStatistical Summary:")
print(state_level_data.describe())

# missing values in each column
print("\nMissing Values per Column:")
print(state_level_data.isnull().sum())


# Question 1.4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.

# Subset tof he DataFrame  abbreviations only and estimates for 2020-2022
state_population_subset = state_level_data[['state_abbreviation', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']]

#pringin initial rows 
print(state_population_subset.head())


# Question 1.5: Show only the 10 largest states by 2021 population estimates,
# in decending order.

# Sorting by 2021 descending order
largest_states_by_2021_population = state_population_subset.sort_values(by='POPESTIMATE2021', ascending=False)

# Selecting top 10 largest states by 2021 population
top_10_largest_states = largest_states_by_2021_population.head(10)

# Printing the result
print(top_10_largest_states)



# Question 1.6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?

# Creating the new popchange column
state_population_subset['POPCHANGE'] = state_population_subset['POPESTIMATE2022'] - state_population_subset['POPESTIMATE2020']

# Calculating the number of states with increase  population
states_gained_population = (state_population_subset['POPCHANGE'] > 0).sum()

# Calculating the number of states that decreased population
states_lost_population = (state_population_subset['POPCHANGE'] < 0).sum()

# Printing the answer
print(f"Number of states that gained population from 2020 to 2022: {states_gained_population}")
print(f"Number of states that lost population from 2020 to 2022: {states_lost_population}")


# Question 1.7: Show all the states that had an estimated change in either
# direction of smaller than 1000 people. 

# Filtering states with pop change < |1000| (small change)
small_pop_change_states = state_population_subset[abs(state_population_subset['POPCHANGE']) < 1000]

# Printing
print(small_pop_change_states)


# Question 1.8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.

# Calculating SD of the pop change
std_dev_pop_change = state_population_subset['POPCHANGE'].std()

# Filtering states with pop change > one SD
states_large_pop_change = state_population_subset[abs(state_population_subset['POPCHANGE']) > std_dev_pop_change]

# Sorting by the absolute value  in descending order
sorted_states_large_pop_change = states_large_pop_change.reindex(
    state_population_subset['POPCHANGE'].abs().sort_values(ascending=False).index
)

# Printing the sorted results 
print(sorted_states_large_pop_change)


#PART 2: Data manipulation

# Question 2.1: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?
# Explain in a brief (1-2 line) comment.



if 'POPCHANGE' in state_population_subset.columns:
    state_population_subset.drop(columns=['POPCHANGE'], inplace=True)

# Ensuring correct format
state_population_subset.columns = ['state_abbreviation', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']

# Reseting the index
state_population_subset.reset_index(drop=True, inplace=True)

# Performing the wide_to_long 
long_format_data = pd.wide_to_long(
    state_population_subset, 
    stubnames='POPESTIMATE', 
    i='state_abbreviation', 
    j='year',
    sep='20'
).reset_index()

# Correcting the year
long_format_data['year'] = long_format_data['year'].astype(str)
long_format_data['year'] = long_format_data['year'].apply(lambda x: int('20' + x))

# Sorting the datafor readability
long_format_data = long_format_data.sort_values(by=['state_abbreviation', 'year'])

# printing the result
print(long_format_data.head())


### Dropping the POPCHANGE column before reshaping because it spans multiple years 
#and is unsuitable for a long format.



# Question 2.2: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 2.1 (without the POPCHANGE column).

# Ensuring 'state_abbreviation' is a column and POPCHANGE is dropped
if 'POPCHANGE' in state_population_subset.columns:
    state_population_subset.drop(columns=['POPCHANGE'], inplace=True)

# Using the melt function 
melted_data = pd.melt(state_population_subset, id_vars=['state_abbreviation'],
                      value_vars=['POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022'],
                      var_name='year', value_name='POPESTIMATE')

# Cleaning up the 'year' column 
melted_data['year'] = melted_data['year'].str.extract('(\d+)').astype(int)

# Sorting the data for better readability
melted_data = melted_data.sort_values(by=['state_abbreviation', 'year'])

# Printing the result 
print(melted_data.head())


# Question 2.3: Open the state-visits.xlsx file in Excel, and fill in the VISITED
# column with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original wide-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.


visits_df = pd.read_excel('/Users/attaullah/Documents/homework-2-attaullahabbasi12/state-visits.xlsx')

# Renameing the column in visits_df 
visits_df.rename(columns={'STATE': 'state_abbreviation'}, inplace=True)

# Merging the dataframes 
merged_data = pd.merge(state_population_subset, visits_df[['state_abbreviation', 'VISITED']],
                       on='state_abbreviation', how='inner')

# Checking for dropped observations
print("Original DataFrame size:", state_population_subset.shape[0])
print("Merged DataFrame size:", merged_data.shape[0])

# Identifying and printing  
missing_states = state_population_subset[~state_population_subset['state_abbreviation'].isin(merged_data['state_abbreviation'])]
print("States dropped from the merge:")
print(missing_states)

# Question 2.4: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state, beginning in different years for
# each state but ending in 2022 for all states.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.

policy_df = pd.read_excel('/Users/attaullah/Documents/homework-2-attaullahabbasi12/policy_uncertainty.xlsx')
print(policy_df)
# Calculating the mean EPU_Composite 
mean_epu_composite = policy_df.groupby(['state', 'year'])['EPU_Composite'].mean().reset_index()

# printing
print(mean_epu_composite)

# Question 2.5) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 


# Question 2.6) Finally, merge this data into your merged data from question 2.3, 
# making sure the merge does what you expect.

# Pivot 
epu_wide_format = mean_epu_composite.pivot_table(index='state', columns='year', values='EPU_Composite')

#result
print(epu_wide_format)

# Question 2.7: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?

# a
# smallest state visited
smallest_visited_state = merged_data[merged_data['VISITED'] == 1].nsmallest(1, 'POPESTIMATE2022')
print("Smallest visited state by 2022 population:", smallest_visited_state[['state_abbreviation', 'POPESTIMATE2022']])

# smallest state not visited
smallest_not_visited_state = merged_data[merged_data['VISITED'] == 0].nsmallest(1, 'POPESTIMATE2022')
print("Smallest not visited state by 2022 population:", smallest_not_visited_state[['state_abbreviation', 'POPESTIMATE2022']])

#b
# three largest states visited
largest_visited_states = merged_data[merged_data['VISITED'] == 1].nlargest(3, 'POPESTIMATE2022')
print("Three largest visited states by 2022 population:")
print(largest_visited_states[['state_abbreviation', 'POPESTIMATE2022']])

# three largest states not visited
largest_not_visited_states = merged_data[merged_data['VISITED'] == 0].nlargest(3, 'POPESTIMATE2022')
print("Three largest not visited states by 2022 population:")
print(largest_not_visited_states[['state_abbreviation', 'POPESTIMATE2022']])

#c #first merging visits and policy data 

# Renaming the column
policy_df.rename(columns={'state': 'state_abbreviation'}, inplace=True)

# Mergeing
merged_visits_policy = pd.merge(policy_df, visits_df, on='state_abbreviation', how='left')

#EPU-C value in 2022 for visited states
average_epu_visited = merged_visits_policy[merged_visits_policy['VISITED'] == 1]['EPU_Composite'].mean()

# average EPU-C value in 2022 for states not visited
average_epu_not_visited = merged_visits_policy[merged_visits_policy['VISITED'] == 0]['EPU_Composite'].mean()

# Compare the averages
if average_epu_visited > average_epu_not_visited:
    print("States you have visited have a higher average EPU-C value in 2022.")
elif average_epu_visited < average_epu_not_visited:
    print("States you have not visited have a higher average EPU-C value in 2022.")
else:
    print("The average EPU-C value in 2022 is the same for both visited and not visited states.")



# Question 2.8: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 2.4 and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.

# Grouping the long-form EPU data by state
grouped_data = mean_epu_composite.groupby('state')

# Defining a function for z score
def calculate_zscore(x):
    mean = x.mean()
    std = x.std()
    return (x - mean) / std

# Applying the function 
mean_epu_composite['EPU_C_zscore'] = grouped_data['EPU_Composite'].transform(calculate_zscore)

# Printing to confirm
print(mean_epu_composite.head())




#### Sources:
    
    #### For 1.2, I initially searched on Google for "how to map FIPS codes to state abbreviations in Python." 
    ### This search led me to the us library documentation, which provides functionality for this purpose. 
    ### Following the documentation, I was able to successfully map the FIPS codes to state abbreviations in the dataset.
    
    ### The solution for Question 2.1, 
    ### was guided by ChatGPT. I asked ChatGPT for assistance on 
    ###"how to reshape data from wide to long format in pandas."
    ###ChatGPT provided instructions on using the wide_to_long function



