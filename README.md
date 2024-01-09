# HTML-Web-Scraping-using-Python-from-the-website-'https://securities.stanford.edu/filings-case.html'
Objective:
The purpose of this Python script is to scrape data related to securities class action filings from the Stanford Securities Class Action Clearinghouse website (https://securities.stanford.edu/). The scraped data includes details such as court information, docket number, judge, filing date, class period start and end dates, case status, and page number.

Dependencies:

The script relies on several Python libraries, including:
BeautifulSoup: For parsing HTML content.
requests: For making HTTP requests.
pandas: For handling data in tabular format.
re: For regular expressions.
quote_plus from urllib.parse: For URL encoding.
sqlalchemy: For interacting with SQL databases.
Database Configuration:

The script connects to a Microsoft SQL Server database using the sqlalchemy library.
The database connection details, such as the server address, database name, username, and password, are specified in the connection_string variable.
Ensure you have the appropriate ODBC driver installed on your system.
Web Scraping:

The script iterates through a range of page numbers (in the example, from page 219 to 220) on the Stanford Securities Class Action Clearinghouse website.
It sends HTTP GET requests to each page, extracts relevant information from the HTML content, and stores the data in a Pandas DataFrame.
The script then inserts the DataFrame into a specified SQL Server database table.
Headers and Cookies:

The script sets headers and cookies in the HTTP requests to simulate a user's interaction with the website.
It's crucial to replace the placeholder cookies and headers with your own valid values.
Processing Details:

The script processes each row in the HTML table, extracting information related to the filing name, Stanford ID, and other relevant details.
It uses a secondary request to obtain additional details for each filing.
The scraped information is cleaned and formatted, including the removal of unwanted tags and spaces.
Database Interaction:

The script uses SQLAlchemy to create a connection to the SQL Server database.
It then inserts the scraped data into the specified database table.
Usage:

Install the required Python libraries (BeautifulSoup, requests, pandas, sqlalchemy).
Set up your database connection details in the connection_string variable.
Replace the placeholder cookies and headers with valid values.
Run the script to start the web scraping process.
Note:

Ensure compliance with the terms of use of the website being scraped.
The script should be customized based on your database structure and the specific requirements of your project.
Handle sensitive information such as database credentials and cookies securely 
