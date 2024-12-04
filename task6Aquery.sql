SELECT 
    br.Card_No AS 'Borrower ID',
    br.Name AS 'Borrower Name',
    COALESCE(SUM(DATEDIFF(bl.Returned_date, bl.Due_Date) * 0.25), 0) AS 'Late Fee Balance ($)'
FROM 
    BORROWER br
LEFT JOIN 
    BOOK_LOANS bl ON br.Card_No = bl.Card_No
WHERE 
    (@BorrowerID IS NULL OR br.Card_No = @BorrowerID)
    AND (@BorrowerName IS NULL OR br.Name LIKE CONCAT('%', @BorrowerName, '%'))
GROUP BY 
    br.Card_No, br.Name
ORDER BY 
    `Late Fee Balance ($)` DESC;
