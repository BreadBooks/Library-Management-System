SELECT 
    Book_Id AS 'Book ID', 
    Branch_Id AS 'Branch ID', 
    Card_No AS 'Card Number', 
    Due_Date AS 'Due Date', 
    Returned_date AS 'Return Date',
    DATEDIFF(Returned_date, Due_Date) AS 'Days Late'
FROM BOOK_LOANS
WHERE Returned_date > Due_Date
AND Due_Date BETWEEN 'start_date_placeholder' AND 'end_date_placeholder';
