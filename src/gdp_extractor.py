import numpy as np
import pandas as pd
import warnings



#ignore warnings

def warn(*args, **kwargs):
    pass
warnings.warn = warn
warnings.filterwarnings('ignore')

#URL for GDP Data
URL="https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"


def fetch_data(url):
    #Read all tables on the page
    tables = pd.read_html(url)

    #Select the third table
    data = tables[3]

    return data

def process_data(data):
     #Replace column headers with columns numbers(0,1,2,...)
    data.columns = range(data.shape[1])

    # Retain columns with index 0 and 2 (name of country and value of GDP quoted by IMF)
    data = data[[0, 2]]

    # Retain rows with index 1 to 10
    top_10 = data.iloc[1:11]  # index 1 to 10 inclusive

     # Convert the selected columns to numpy arrays
    countries = np.array(top_10.iloc[:, 0])  # First column (Country)
    gdp_values = np.array(top_10.iloc[:, 1])  # Second column (GDP)

     # Create a new DataFrame with only the two selected columns
    top_10 = pd.DataFrame({
        "Country": countries,
        "GDP (Million USD)": gdp_values
    })

    # Change the data type of the 'GDP (Million USD)' column to integer.
    top_10['GDP (Million USD)'] = top_10['GDP (Million USD)'].astype(int)

    #Convert the GDP value in Million USD to Billion USD
    top_10[['GDP (Million USD)']] = top_10[['GDP (Million USD)']]/1000

    #Round the value to 2 decimal places.
    top_10[['GDP (Million USD)']] = np.round(top_10[['GDP (Million USD)']], 2)

    # Rename the column header from 'GDP (Million USD) to 'GDP (Billion USD)'
    top_10 = top_10.rename(columns = {'GDP (Million USD)' : 'GDP (Billion USD)'})

    return top_10
def main():
    data = fetch_data(URL)
    if data is not None:
        top_10 = process_data(data)
        print("Top 10 Largest Economies by GDP (in Million USD):")
        print(top_10)

if __name__ == "__main__":
    main()
