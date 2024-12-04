SELECT 
    b.Book_Id AS 'Book ID',
    b.Title AS 'Book Title',
    bl.Branch_Id AS 'Branch ID',
    bl.Due_Date AS 'Due Date',
    DATEDIFF(CURDATE(), bl.Due_Date) * 0.25 AS 'Late Fee ($)'
FROM 
    BOOK b
JOIN 
    BOOK_LOANS bl ON b.Book_Id = bl.Book_Id
WHERE 
    (@BorrowerID IS NULL OR bl.Card_No = @BorrowerID)
    AND (@BookID IS NULL OR b.Book_Id = @BookID)
    AND (@BookTitle IS NULL OR b.Title LIKE CONCAT('%', @BookTitle, '%'))
ORDER BY 
    `Late Fee ($)` DESC;
