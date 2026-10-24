Homework 03 — Purchase Analysis with PySpark
About this project
In this homework, I used PySpark to analyze purchase data from three CSV files. My goal was to calculate spending by product category and find out which categories accounted for the largest share of purchases among customers aged 18–25.
Tools and data
I used Python and PySpark. I worked with three datasets stored in the data/ folder:
- users.csv — customer IDs, names, ages, and email addresses.
- purchases.csv — purchase IDs, customer and product IDs, dates, and quantities.
- products.csv — product IDs, names, categories, and prices.
The CSV files need to be placed in data/ before running the script.
How I ran the project
I installed the required Python packages and ran the main script from the project folder. PySpark also requires Java.
python -m pip install -r requirements.txt
python main.py
My workflow and results
1. Loading the original data
I loaded each CSV as a separate Spark DataFrame and displayed the first 20 rows to inspect the columns and values.

Users

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/01-original-users.png

Purchases

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/02-original-purchases.png

Products

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/03-original-products.png
2. Cleaning missing values
I removed rows containing missing values from each DataFrame. The row counts changed as follows:
Dataset	Before cleaning	After cleaning	Removed
Users	100	95	5
Purchases	200	195	5
Products	50	47	3


Cleaned users

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/04-cleaned-users.png

Cleaned purchases

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/05-cleaned-purchases.png

Cleaned products

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/06-cleaned-products.png
3. Joining the datasets
I joined the cleaned purchase records with the product and user tables using product_id and user_id. I then calculated the amount for each purchase as quantity * price.

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/07-joined-data.png
4. Total spending by category
I grouped the joined records by product category and summed the purchase amounts. I rounded the displayed values to two decimal places below for readability.
Category	Total spending
Beauty	441.70
Clothing	696.10
Electronics	1,141.90
Home	1,438.90
Sports	1,755.50


5. Spending by customers aged 18–25
Next, I filtered the joined records to include customers aged 18 through 25, including both endpoints. I calculated their spending totals by category.
Category	Spending, ages 18–25
Beauty	41.40
Clothing	245.00
Electronics	249.60
Home	361.10
Sports	310.50


6. Percentage shares and top three categories
I divided each category's spending by the total spending of customers aged 18–25 and multiplied by 100. I then sorted the results by percentage in descending order and selected the first three categories.
Rank	Category	Share of spending
1	Home	29.90%
2	Sports	25.71%
3	Electronics	20.67%


The screenshot below shows my terminal output for steps 4–6, including the full percentage distribution and top three categories.

https://github.com/kattykatty-hub/goit-de-hw-03/blob/main/screenshots/08-sales-analysis.png
What I learned
This exercise helped me practice loading CSV data into Spark DataFrames, cleaning missing values, joining tables, creating calculated columns, filtering by age, and aggregating results. I also learned how to turn grouped totals into percentages and rank categories by spending share.

From my results, Home was the largest category for customers aged 18–25 at 29.90%, followed by Sports at 25.71% and Electronics at 20.67%. Together, these three categories represented 76.28% of spending in that age group.

Note: The tables in this README are rounded for presentation; the screenshots show the original Spark output, including floating-point precision.