from flask import Blueprint, render_template
from config.db_config import connect_to_database, close_connection
import plotly.express as px
import pandas as pd
from  models.helper_functions import map_country_names

main_bp = Blueprint('main', __name__)

# Home Route
@main_bp.route('/')
def home():
    """
    Home endpoint to check if the API is running.

    Returns:
        Renders the home HTML page.
    """
    return render_template('index.html')  # Render HTML template for the home page

# About Us Route
@main_bp.route('/about')
def about_us():
    """
    Home endpoint to check if the API is running.

    Returns:
        Renders the home HTML page.
    """
    return render_template('about_us.html')  # Render HTML template for the home page

                        
# Profile Page
@main_bp.route('/profile')
def profile():
    # Database connection
    conn = connect_to_database()
    # Query to fetch user profile and order history
    query_profile_order_history = '''
    SELECT 
        u.UserID, 
        u.UserName, 
        u.Email, 
        u.Password,
        u.Role,
        u.Created_At, 
        c.CountryID, 
        s.SaleID, 
        s.Sale_Date, 
        b.Title AS Book_Title, 
        s.Sale_Quantity, 
        s.Total_Price
    FROM Users u
    JOIN Countries c ON u.CountryID = c.CountryID
    LEFT JOIN Sales s ON u.UserID = s.UserID
    LEFT JOIN Books b ON s.BookID = b.BookID

    ORDER BY s.Sale_Date DESC;
    '''

    # Fetching data from the database
    profile_df = pd.read_sql_query(query_profile_order_history, conn)
    # Create a new column for Country names in the dataframe
    #profile_df['CountryName'] = map_country_names(profile_df)
    profile_df['CountryName'] = map_country_names(profile_df)
    #profile_df['CountryName'] = profile_df['CountryID'].map({v: k for k, v in country_map.items()})
    # Drop CountryID col
    profile_df.drop(columns=['CountryID'], inplace=True)
    # Render the order profile
    return render_template('profile.html', profiles=profile_df.to_dict(orient='records'))

# Dashboard Page
@main_bp.route('/dashboard')
def dashboard():
    # Database connection
    conn = connect_to_database()
    
    # Query to get total number of authors, users, and books
    query_total_authors = 'SELECT COUNT(*) FROM Authors;'
    query_total_users = 'SELECT COUNT(*) FROM Users;'
    query_total_books = 'SELECT COUNT(*) FROM Books;'
    
    total_authors = pd.read_sql_query(query_total_authors, conn).iloc[0, 0]
    total_users = pd.read_sql_query(query_total_users, conn).iloc[0, 0]
    total_books = pd.read_sql_query(query_total_books, conn).iloc[0, 0]

    # Sales Trend (Line Chart)
    query_sales_trends_daily = '''
    SELECT strftime('%Y-%m-%d', s.Sale_Date) AS Day, SUM(s.Total_Price) AS Total_Sales
    FROM Sales s
    GROUP BY Day
    ORDER BY Day;
    '''
    sales_trends_df_daily = pd.read_sql_query(query_sales_trends_daily, conn)
    fig1 = px.line(sales_trends_df_daily, x='Day', y='Total_Sales',
                   labels={'Day': 'Day', 'Total_Sales': 'Total Sales'}, markers=True)
    fig1.update_layout(title_x=0.5)
    # Add annotations for the max and min sales values
    max_sales = sales_trends_df_daily['Total_Sales'].max()
    min_sales = sales_trends_df_daily['Total_Sales'].min()
    max_sales_day = sales_trends_df_daily[sales_trends_df_daily['Total_Sales'] == max_sales]['Day'].values[0]
    min_sales_day = sales_trends_df_daily[sales_trends_df_daily['Total_Sales'] == min_sales]['Day'].values[0]

    fig1.add_annotation(
        x=max_sales_day,
        y=max_sales,
        text=f"Max: {max_sales}",
        showarrow=True,
        arrowhead=2,
        font=dict(size=12, color="red"),
        bgcolor="white",
        bordercolor="red",
        borderwidth=1
    )

    fig1.add_annotation(
        x=min_sales_day,
        y=min_sales,
        text=f"Min: {min_sales}",
        showarrow=True,
        arrowhead=2,
        font=dict(size=12, color="blue"),
        bgcolor="white",
        bordercolor="blue",
        borderwidth=1
    )

    fig1.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
        ),
        showlegend=False  
    )

    # Best Selling Books (Bar Chart)
    query_best_selling_books = '''
    SELECT b.BookID, b.Title, SUM(s.Total_Price) AS Total_Sales, SUM(s.Sale_Quantity) AS Total_Quantity_Sold
    FROM Sales s
    JOIN Books b ON s.BookID = b.BookID
    GROUP BY b.BookID
    ORDER BY Total_Sales DESC
    LIMIT 10;
    '''
    best_selling_books_df = pd.read_sql_query(query_best_selling_books, conn)
    fig2 = px.bar(best_selling_books_df, x='Title', y='Total_Quantity_Sold',
                  labels={'Title': 'Book Name', 'Total_Quantity_Sold': 'Total Quantity Sold'}, color='Total_Quantity_Sold', color_continuous_scale='Viridis')
    fig2.update_layout(title_x=0.5)

    # Top Authors (Bar Chart)
    query_top_performing_authors = '''
    SELECT a.AuthorID, (a.First_Name || a.Last_Name) AS FullName, SUM(s.Total_Price) AS Total_Sales, AVG(r.Rating) AS Average_Rating
    FROM Authors a
    JOIN Books b ON a.AuthorID = b.AuthorID
    JOIN Sales s ON b.BookID = s.BookID
    JOIN Reviews r ON b.BookID = r.BookID
    GROUP BY a.AuthorID
    ORDER BY Total_Sales DESC, Average_Rating DESC
    LIMIT 10;
    '''
    top_performing_authors_df = pd.read_sql_query(query_top_performing_authors, conn)
    fig3 = px.bar(top_performing_authors_df, x='FullName', y='Total_Sales',
                  labels={'FullName': 'Author Name', 'Total_Sales': 'Total Sales'}, color='Average_Rating', color_continuous_scale='Viridis')
    fig3.update_layout(title_x=0.5)

    # Geographical Distribution of Authors by Nationality
    query_geographical_distribution  = '''
    SELECT a.CountryID, COUNT(a.AuthorID) AS Number_of_Authors
    FROM Authors a
    GROUP BY a.CountryID
    ORDER BY Number_of_Authors DESC;
    '''
    geographical_distribution_df = pd.read_sql_query(query_geographical_distribution, conn)
    # Assuming 'country_map' and 'geographical_distribution_df' are defined
    geographical_distribution_df['CountryName'] = map_country_names(geographical_distribution_df)

    #geographical_distribution_df['CountryName'] = geographical_distribution_df['CountryID'].map({v: k for k, v in country_map.items()})
    fig4 = px.pie(geographical_distribution_df, names='CountryName', values='Number_of_Authors',
                title="Geographical Distribution of Authors by Nationality")
    fig4.update_layout(title_x=0.5)

    # Close the connection
    close_connection(conn)

    # Render dashboard with charts and summary data
    return render_template('dashboard.html', 
                           total_authors=total_authors,
                           total_users=total_users,
                           total_books=total_books,
                           sales_trends_chart=fig1.to_html(full_html=False),
                           best_selling_books_chart=fig2.to_html(full_html=False),
                           top_authors_chart=fig3.to_html(full_html=False),
                           Geographical_Distribution_of_Authors_by_Nationality=fig4.to_html(full_html=False))

@main_bp.route('/order_history')
def order_history():
    # Database connection
    conn = connect_to_database()

    # Query to get order history for users
    query_order_history = '''
    SELECT 
        u.UserID,
        u.UserName,
        s.SaleID,
        s.Sale_Date,
        b.Title AS Book_Title,
        s.Sale_Quantity,
        s.Total_Price,
        c.CountryID
    FROM 
        Sales s
    JOIN 
        Users u ON s.UserID = u.UserID
    JOIN 
        Books b ON s.BookID = b.BookID
    JOIN 
        Countries c ON s.CountryID = c.CountryID
    ORDER BY 
        s.Sale_Date DESC;  -- Orders by the most recent sales first
    '''

    order_history_df = pd.read_sql_query(query_order_history, conn)
    # Create a new column for Country names in the dataframe
    order_history_df['CountryName'] = map_country_names(order_history_df)
    #order_history_df['CountryName'] = order_history_df['CountryID'].map({v: k for k, v in country_map.items()})
    # Drop CountryID col
    order_history_df.drop(columns=['CountryID'], inplace=True)
    conn.close()

    # Render the order history page
    return render_template('order_history.html', order_history=order_history_df.to_dict(orient='records'))

