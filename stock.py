#import the libaray
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


#To read the csv file
final_stock  = pd.read_csv("All_Tickers.csv")

#To convert the date column is in datetime format
final_stock['date'] = pd.to_datetime(final_stock['date'])

# Exract year from the date column
final_stock['year'] = final_stock['date'].dt.year

# Exract year from the date column
final_stock['months'] = final_stock['date'].dt.month

# Exract year from the date column
final_stock['day'] = final_stock['date'].dt.day



# ✅ Sidebar Navigation (Defined Only Once)
st.sidebar.title("📊 Stock Market Analysis")

# ✅ Sidebar Navigation 
st.sidebar.subheader("Select an Analysis")

#main page 
page = st.sidebar.radio("Navigation", ["🏠 Home", "📈 Analysis", "📊 Market Summary"])

# ✅ Home Page
if page == "🏠 Home":
    # Centered and colored title
    st.markdown("<h1 style='text-align: center; color: violet;'>🏠 Welcome to Stock Market Analysis Dashboard!</h1>", unsafe_allow_html=True)
    
    # Streamlit Title
    st.title(':rainbow[This dashboard helps you analyze stock trends, volatility, returns, sector performance, and more.]')

    #To show the image
    st.image("C:/Users/NAVEEN/OneDrive/Desktop/stoke-market-1-1.png")
    

# ✅ Market Summary Page
elif page == "📊 Market Summary":

      # Centered and colored title
    st.markdown("<h1 style='text-align: center; color: Red;'>Stock Market Summary</h1>", unsafe_allow_html=True)

    #To create the Radio button on sidebar
    Market_part = st.sidebar.radio("Market_details",["Top_10_Green_Stocks","Top_10_Loss_Stocks","Avg_Volume_per_stocks","Avg_prices_per_stocks","NO_Green_stocks&Loss_stocks" ])
    
    # To create the List
    year_price = []
    tickers = []
    #using for loop to calculate open and closing stock year wise
    for i in final_stock['Ticker'].unique():
        # using this variable(Ticker_unique) to get each Ticker values
        Ticker_unique = final_stock[final_stock['Ticker'] == i]
        #using this varaible(year_trend)to calculate the value for yearwise using iloc function(row_wise_index)
        year_trend = ((Ticker_unique.iloc[-1]['close'] - Ticker_unique.iloc[0]['open'])/Ticker_unique.iloc[-1]['open'])*100
        #To append the ticker_value
        tickers.append(i)
        # To append the year_trend
        year_price.append(year_trend) 

    # To creat the dataframe 
    year_data = pd.DataFrame({'Ticker': tickers, 'stock_price_year': year_price})

    # Top_10_Green_Stocks
    if Market_part == "Top_10_Green_Stocks" :
    # Top_10 Green_Stcoks for year_wise
        Top_10_Green_Stocks = year_data.sort_values(by= 'stock_price_year', ascending=False).head(10)
        #To reset the index value 
        Top_10_Green_Stocks= Top_10_Green_Stocks.reset_index(drop=True)
        # Streamlit Title
        st.title(':rainbow[Top_10_Green_Stocks]')
        #To show the Dataframe
        st.write(Top_10_Green_Stocks)
        
        # Create Plotly Bar Plot
        fig = px.bar(
            Top_10_Green_Stocks,
            x="Ticker",
            y="stock_price_year",
            color="Ticker",
            color_discrete_sequence=px.colors.sequential.Viridis,
            labels={"Ticker": "Stock Ticker", "stock_price_year": "Stock Price Yearly Return"},
            title="Top 10 Green Stocks by Yearly Return"
        )

        # Improve readability
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Stock Price Yearly Return",
            xaxis_title="Stock Ticker",
            template="plotly_white"
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig)
        
    # Top 10 Loss stocks
    elif Market_part == "Top_10_Loss_Stocks" :
        # Top_10 Loss_ Stcoks for year_wise
        Top_10_Loss_Stocks = year_data.sort_values(by='stock_price_year', ascending=False).tail(10)
        #To reset the index value 
        Top_10_Loss_Stocks = Top_10_Loss_Stocks.reset_index(drop=True)
        # Streamlit Title
        st.title(':rainbow[Top_10_Loss_Stocks]')
        #To show the dataframe
        st.write(Top_10_Loss_Stocks)

       # Create Plotly Bar Plot
        fig = px.bar(
            Top_10_Loss_Stocks,
            x="Ticker",
            y="stock_price_year",
            color="Ticker",
            text="stock_price_year",  # Show values on bars
            color_discrete_sequence=px.colors.sequential.Cividis,  
            labels={"Ticker": "Stock Ticker", "stock_price_year": "Stock Price Yearly Return"},
            title="Top 10 Loss Stocks by Yearly Return"
        )

        # Improve readability
        fig.update_traces(textposition="outside")  # Display values on top of bars
         #for layout
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Stock Price Yearly Return",
            xaxis_title="Stock Ticker",
            template="plotly_white"
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig)


    # Average price for Each stocks
    elif Market_part == "Avg_prices_per_stocks" :
       #To take the average value of close cloumn based on Ticker cloumn
       Avg_prices_per_stocks = final_stock.groupby("Ticker")["close"].mean().reset_index()

       #To Rename the cloumn
       Avg_prices_per_stocks = Avg_prices_per_stocks.rename(columns={"close": "Avg_Close_Price"})

       # Streamlit Title
       st.title(':rainbow[Average price for All Stocks]')

       # To show dataframe 
       st.write(Avg_prices_per_stocks)

    # Creating the visualization
       fig, ax = plt.subplots(figsize=(12, 6))
       sns.barplot(x=Avg_prices_per_stocks["Ticker"], y=Avg_prices_per_stocks["Avg_Close_Price"], palette="viridis", ax=ax)
       ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
       plt.title("Average price_stocks for Each Tickers")

        # Adding value labels on top of each bar
       for index, row in Avg_prices_per_stocks.iterrows():
            ax.text(index, row["Avg_Close_Price"], f'{row["Avg_Close_Price"]:.2f}', ha='center', va='bottom', fontsize=5, color='black')

       # Display the chart in Streamlit
       st.pyplot(fig)

    # Average volume for Each stocks
    elif Market_part == "Avg_Volume_per_stocks":
        #To take the average values on vlolume cloumn based on Each Ticker
        Avg_Volume_per_stocks = final_stock.groupby("Ticker")["volume"].mean().round(2).reset_index()

        #To Rename the cloumn
        Avg_Volume_per_stocks = Avg_Volume_per_stocks.rename(columns={"volume":"Avg_Volume"})

        # Streamlit Title
        st.title(':rainbow[Average Volume for All Stocks]')

        # To show dataframe 
        st.write(Avg_Volume_per_stocks)

        # Creating the visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=Avg_Volume_per_stocks["Ticker"], y=Avg_Volume_per_stocks["Avg_Volume"], palette="viridis", ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.title("Average_volume for Each Tickers")

        # Adding value labels on top of each bar
        for index, row in Avg_Volume_per_stocks.iterrows():
                ax.text(index, row["Avg_Volume"], f'{row["Avg_Volume"]:.2f}', ha='center', va='bottom', fontsize=5, color='black')
        # Display the chart in Streamlit
        st.pyplot(fig)

    # Total number of Green and loss stocks
    elif Market_part == "NO_Green_stocks&Loss_stocks":
         #To closing cloumn is greater than open it green stocks and it sum to find the total green stocks
         green_stocks = (final_stock["close"] > final_stock["open"]).sum()
         #To closing cloumn is lesser than open it green stocks and it sum to find the total red stocks
         red_stocks = (final_stock["close"] < final_stock["open"]).sum()

         # Creating a DataFrame with an index
         data = pd.DataFrame({
            "Stock Type": ["Green Stocks", "Red Stocks"],
            "Count": [green_stocks, red_stocks]}).set_index("Stock Type")
         
         # Streamlit Title
         st.title(':rainbow[Total Number of Green&Red Stocks]')
         
         #To show Dataframe
         st.write(data)

         # Create the pie chart
         fig, ax = plt.subplots()
         ax.pie([green_stocks, red_stocks], labels=["Green Stocks", "Red Stocks"], autopct='%1.1f%%', colors=["green", "red"], startangle=90)
         ax.set_title("Green vs. Red Stocks")

        # Display in Streamlit
         st.pyplot(fig)
       
       

# ✅ Analysis Page 
elif page == "📈 Analysis":
   
    # TO create the radio in sidebar under analysis butt0n
   Analyis_part = st.sidebar.radio("Analysis",["Volatility Analysis","Cumulative Return Over Time","Sector-wise Performance","Stock Price Correlation","Top 5 Month_Wise_Gainers and Losers "])
   
   
    #  Volatility Analysis:
   if Analyis_part == "Volatility Analysis" :

        # Centered and colored title
        st.markdown("<h1 style='text-align: center; color: blue;'>Volatility Analysis</h1>", unsafe_allow_html=True)

        #To create the New column using the prevoius column with shift operation
        final_stock['pre_close'] = final_stock['close'].shift(1)

        #using For loop to do calculate daily Return for each stock in single day
        for i in final_stock["Ticker"]:
            final_stock['daily_return'] = (final_stock['close'] - final_stock['pre_close']) / final_stock['pre_close']

        # After that i will check any null values in my dataset

        # we have 1(Null_values) in my first Row of dataset (final_Stock.iloc[0])

        #so i will drop my null values using dropna method
        final_stock.dropna(inplace=True)

        #To calculate the mean value for daily_return for each Tickers(stocks)
        #using reset_index to get proper index values
        AVG_per_Stocks_day = final_stock.groupby('Ticker')["daily_return"].mean().reset_index()

        #Top 10 Most volatile stocks over the year using head function
        Top_10_Most_Volatile_Stocks = AVG_per_Stocks_day.sort_values("daily_return",ascending=False).head(10).reset_index(drop=True)
        Top_10_Most_Volatile_Stocks = Top_10_Most_Volatile_Stocks.rename(columns={"daily_return": 'volatile_return'})

        # Streamlit Title
        st.title(':rainbow[Top_10_Most_Volatile_Stocks]')

        #to show dataframe
        st.write(Top_10_Most_Volatile_Stocks)

        # Bar chart
        fig = px.bar(Top_10_Most_Volatile_Stocks, 
                    x="Ticker", 
                    y="volatile_return", 
                    title="Top 10 Most Volatile Stocks Over the Year", 
                    labels={"daily_return": "Average Daily Return"},
                    text_auto=True,
                    color="volatile_return",
                    color_continuous_scale="viridis" )
        st.plotly_chart(fig)

   # comulative Return 
   elif Analyis_part == "Cumulative Return Over Time":
        
        # Centered and colored title
        st.markdown("<h1 style='text-align: center; color: green;'>Cumulative Return for Top 5 Performing Stocks</h1>", unsafe_allow_html=True)
      
        # To create the list 
        comulative_return = []
        comulative_ticker = []

        # using For loop for Each unique stock
        for i in final_stock["Ticker"].unique():
            com_Ticker = final_stock[final_stock["Ticker"] == i]
            
            # Correct return formula
            com_return = (com_Ticker.iloc[-1]["close"] - com_Ticker.iloc[0]["close"]) / com_Ticker.iloc[0]["close"]
            
            # Append results
            comulative_ticker.append(i)  # Append Ticker name
            comulative_return.append(com_return)  # Append calculated return

        # Create DataFrame
        comulative_return_year = pd.DataFrame({
            "Ticker": comulative_ticker, 
            "Cumulative Return": comulative_return
        })

        #To get the top 5 stocks comulative stocks based on sort function
        top_5_stocks = comulative_return_year.sort_values(by="Cumulative Return", ascending=False).head(5)

        # Streamlit Title
        st.title(':rainbow[Top 5 Performing Stocks]')

        #To show the dataframe
        st.write(top_5_stocks)

        # Create the line plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_facecolor('black')
        sns.lineplot(data= top_5_stocks , x="Ticker", y="Cumulative Return" , marker="o")


        # Formatting
        ax.set_title("Top 5 Performing Stocks Based on Cumulative Return")
        ax.set_xlabel("Ticker")
        ax.set_ylabel("Cumulative Return")
        ax.tick_params(axis="x", rotation=45)
        ax.legend(title="Ticker")
        ax.grid()

        # Show plot in Streamlit
        st.pyplot(fig)

    # sector wise performance part
   elif Analyis_part == "Sector-wise Performance":

    # Centered and colored title
    st.markdown("<h1 style='text-align: center; color: orange;'>Sector-wise Performance</h1>", unsafe_allow_html=True)

    #To Read the csv file
    sector = pd.read_csv("C:/Users/NAVEEN/Downloads/Sector_data - Sheet1 (2).csv")

    #from this csv we can drop the cloumn(company), the cloumn not use in feature pupurose
    sector.drop("COMPANY",axis=1,inplace=True)
    # To Rename the cloumn name for Feature pupurose(do the function two dataframe)
    sector.rename(columns={"Symbol":"Ticker"},inplace=True)

    #using split function to split data in ticker cloumn
    sector["Ticker"] = sector["Ticker"].str.split(":").str[1].str.strip()



    # Initialize an empty dictionary
    sec_ = {} 
    # Iterate over the DataFrame rows
    for i, row in sector.iterrows():  
    # Assign values correctly
        sec_[row[1]] = row[0] 


    # To create the cloumn in dataframe and using (None) to avoid the key error
    final_stock["sector"] = None  

    #using For loop to iterate the ticker values for mapping
    for i in final_stock["Ticker"]:

        # The iterate values is avaliable in dictionary(sec_)
        if i in sec_: 
            final_stock.loc[final_stock["Ticker"] == i, "sector"] = sec_[i]
        else:
            print(f"Warning: '{i}' not found in sector mapping")

        
    # To get the unquie values of sectors for the purpopse of using sidebar button
    unique_sectors = final_stock["sector"].unique()

    # Sidebar radio button for sector selection
    selected_sector = st.sidebar.radio("Select a Sector", unique_sectors)

# Initialize lists to store results
    overall_returns = []
    sectors = []
    tickers = []

    # Loop through unique Ticker-Sector combinations
    for ticker in final_stock["Ticker"].unique():
        for sector in final_stock["sector"].unique():
            
            # Filter data for the given Ticker and Sector across all years
            overall_data = final_stock[(final_stock["Ticker"] == ticker) & (final_stock["sector"] == sector)]
            
            # Check if there are at least two rows 
            try:
                # Calculate overall return from first available close to last available close
                overall_return = ((overall_data.iloc[-1]["close"] - overall_data.iloc[0]["close"]) / overall_data.iloc[0]["close"]) * 100
                
                # Append values to lists
                tickers.append(ticker)
                sectors.append(sector)
                overall_returns.append(overall_return)

            # Skip this iteration if there's not enough data
            except:
                continue

    # Create DataFrame for results
    sector_wise_overall_return = pd.DataFrame({
        "Ticker": tickers,
        "Sector": sectors,
        "Overall Return (2023-2024)": overall_returns
    })

    # Filter DataFrame based on selected sector
    filtered_sector_data = sector_wise_overall_return[sector_wise_overall_return["Sector"] == selected_sector]

     # Streamlit Title
    st.title(f':rainbow[sector performance:{selected_sector}]')

    # Display filtered data
    st.write(filtered_sector_data)

    # Create a Plotly bar chart
    fig = px.bar(
        filtered_sector_data,  # Your filtered DataFrame
        x="Ticker",
        y="Overall Return (2023-2024)",
        color="Sector",  # Equivalent to hue in Seaborn
        title="Overall Stock Returns (2023-2024)",
        labels={"Overall Return (2023-2024)": "Return (%)"},
        text=filtered_sector_data["Overall Return (2023-2024)"].apply(lambda x: f"{x:.2f}%"),  # Display as percentage
        barmode="group",  # Ensures grouped bars (not stacked)
        color_discrete_sequence=px.colors.qualitative.Set1  # Custom color scheme
    )

    # Update layout for better readability
    fig.update_traces(textposition="outside")  # Show percentage labels outside bars
    fig.update_layout(
        xaxis_tickangle=-90,  # Rotate x-axis labels for readability
        xaxis_title="Ticker",
        yaxis_title="Return (%)",
        legend_title="Sector"
    )

    # Display Plotly figure in Streamlit
    st.plotly_chart(fig)


   

   # stock price correlation part
   elif Analyis_part == "Stock Price Correlation" :
    # Centered and colored title
    st.markdown("<h1 style='text-align: center; color: Red;'>Stock Price Correlation</h1>", unsafe_allow_html=True)
    
    # Pivot Data: Each stock has a separate column for 'close' price
    df_pivot = final_stock.pivot(index="date", columns="Ticker", values="close")

    # Compute the correlation matrix
    correlation_matrix = df_pivot.corr()

    # Streamlit Title
    st.title(':rainbow[Relationship Between Stocks]')

    #To show the Dataframe
    st.write(correlation_matrix)

    # Taking corrlation matrix column values for the fliteration
    columns = correlation_matrix.columns
    # Create the list
    data = []
    # Using For loop for iterate both rows and values
    for i,row in correlation_matrix.iterrows():
        for cloumn in columns :
            #To add the values in list with dictionary format
            data.append({
                    "row" : i,
                    "cloumn" : cloumn,
                    "corr" : row[cloumn]


            })
    #To create the Dataframe
    corr_data = pd.DataFrame(data)

        
    # Drop rows where corr = 1 (Self-correlation)
    corr_data = corr_data[corr_data["corr"] != 1.000000]


    # Function to categorize correlation values
    def categorize_correlation(value):
        if value >= 0.8:
            return "Positive Correlation"
        elif 0.5 <= value < 0.8:
            return "Moderate Correlation"
        elif -0.5 < value < 0.5:
            return "No Correlation"
        else:
            return "Negative Correlation"
        

    # Apply categorization function
    corr_data["Category"] = corr_data["corr"].apply(categorize_correlation)

    # Sidebar selection for categories
    selected_category = st.sidebar.selectbox("Select Correlation Category", ["Positive", "Moderate", "No", "Negative"])

    # Filter data based on selection
    if selected_category == "Positive":
        filtered_data = corr_data[corr_data["Category"] == "Positive Correlation"]

    elif selected_category == "Moderate":
        filtered_data = corr_data[corr_data["Category"] == "Moderate Correlation"]

    elif selected_category == "No":
        filtered_data = corr_data[corr_data["Category"] == "No Correlation"]

    else:
        filtered_data = corr_data[corr_data["Category"] == "Negative Correlation"]

    # Sort by correlation value in descending order and take the top 20
    filtered_data = filtered_data.sort_values("corr", ascending=False).head(20).reset_index(drop=True)

    # Display top 20 rows of the selected category
    st.write(f"### Top 20 {selected_category} Correlation Stocks")

    #To show the dataframe
    st.write(filtered_data.head(20))

    # Visualization using Plotly Bar Chart
    fig = px.bar(
        filtered_data.head(20), 
        x="corr", 
        y="row", 
        color="corr",
        orientation="h",
        color_continuous_scale="Viridis",
        title=f"Top 20 {selected_category} Stock Correlation"
    )

    # Customize labels
    fig.update_layout(xaxis_title="Correlation Value", yaxis_title="Stock Pairs")

    # Show Plot in Streamlit
    st.plotly_chart(fig)


    # Visualization: Histogram (Correlation Frequency)

    if "Stock Pair" not in filtered_data.columns:
     filtered_data["Stock Pair"] = filtered_data["row"] + " - " + filtered_data["cloumn"]

    # Histogram Plot
    fig_hist = px.histogram(
        filtered_data, 
        x="corr", 
        color="Stock Pair",  
        nbins=10,  
        title=f"Correlation Distribution for {selected_category} Stocks",
        labels={"corr": "Correlation Value", "Stock Pair": "Stock Pairs"},
        color_discrete_sequence=px.colors.qualitative.Set1  
    )

    # Update Layout
    fig_hist.update_layout(xaxis_title="Correlation Value", yaxis_title="Frequency", bargap=0.2)

    # Show Histogram in Streamlit
    st.plotly_chart(fig_hist)


   
   # Top 5 Month_Wise_Gainers and Losers part
   elif Analyis_part == "Top 5 Month_Wise_Gainers and Losers ": 
     # Centered and colored title
    st.markdown("<h1 style='text-align: center; color: violet;'>Top 5 Month_Wise_Gainers and Losers </h1>", unsafe_allow_html=True)

    # Title
    st.title("Top 5 Month-Wise Gainers and Losers")

    # Compute monthly returns
    final_stock["month_return"] = ((final_stock["close"] - final_stock["open"]) / final_stock["open"]) * 100

    # Group by Ticker and Month
    month_wise_return = final_stock.groupby(["Ticker", "month"])["month_return"].mean().reset_index()

    # Get unique months
    month_sectors = final_stock["month"].unique()

    # Sidebar for month selection
    selected_month = st.sidebar.radio("Select Month", month_sectors)

    # Filter DataFrame based on selected month
    month_sector_data = month_wise_return[month_wise_return["month"] == selected_month]
    
    # Streamlit Title
    st.title(f':rainbow[TOP 5 GAINERS MONTH: {selected_month}]')

   

    # Get Top 5 Gainers
    month_Gainer = month_sector_data.sort_values("month_return", ascending=False).head(5).reset_index(drop=True)
    month_Gainer["month_return"] = month_Gainer["month_return"].apply(lambda x: f"{x:.2f}%")  # Convert to percentage format
    st.write(month_Gainer)  # Display dataframe

     # Streamlit Title
    st.title(f':rainbow[TOP 5 LOSERS MONTH: {selected_month}]')

    # Get Top 5 Losers
    month_losers = month_sector_data.sort_values("month_return", ascending=True).head(5).reset_index(drop=True)
    month_losers["month_return"] = month_losers["month_return"].apply(lambda x: f"{x:.2f}%")
    st.write(month_losers)  # Display dataframe

    # Create subplots (1 row, 2 columns)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot Gainers
    ax1 = sns.barplot(data=month_Gainer, x="month", y="month_return", hue = "Ticker",ax=axes[0])
    axes[0].set_title(f"Top 5 Gainers - {selected_month}")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

    # Add labels on bars
    for container in ax1.containers:
        ax1.bar_label(container, fmt="%.2f", fontsize=10, padding=3)

    # Plot Losers
    ax2 = sns.barplot(data=month_losers, x="month", y="month_return", hue = "Ticker", ax=axes[1])
    axes[1].set_title(f"Top 5 Losers - {selected_month}")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)

    # Add labels on bars
    for container in ax2.containers:
        ax2.bar_label(container, fmt="%.2f", fontsize=10, padding=3)

    # Adjust layout
    plt.tight_layout()

    # Show plot in Streamlit
    st.pyplot(fig)
