-- Step 1: Insert the book into the BOOK table
INSERT INTO BOOK (Title, Publisher_Name)
VALUES ('Sample Title', 'Sample Publisher');

-- Step 2: Fetch the last inserted Book_Id
SELECT LAST_INSERT_ID() AS Book_Id;

-- Step 3: Insert the book's author into the BOOK_AUTHORS table
-- Replace `LAST_INSERT_ID()` with the retrieved Book_Id from the previous step
INSERT INTO BOOK_AUTHORS (Book_Id, Author_Name)
VALUES (LAST_INSERT_ID(), 'Sample Author');

-- Step 4: Fetch all Branch_Id from the LIBRARY_BRANCH table
SELECT Branch_Id FROM LIBRARY_BRANCH;

-- Step 5: Insert 5 copies of the book into the BOOK_COPIES table for each branch
-- Repeat the following query for each Branch_Id
INSERT INTO BOOK_COPIES (Book_Id, Branch_Id, No_Of_Copies)
VALUES (LAST_INSERT_ID(), 1, 5);  -- Replace `1` with the actual Branch_Id
