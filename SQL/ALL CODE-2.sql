//1. Basic Logic (AND, OR) //

SELECT * FROM [dbo].[guest]
WHERE [first_name] = 'Liam' AND [last_name] = 'Smith';

SELECT * FROM [dbo].[room]
WHERE [room_type] = 'Suite' OR [room_type] = 'Penthouse';

// 2. Lists (IN, NOT IN) //

SELECT * FROM [dbo].[room]
WHERE [floor_number] IN (1, 2, 5);

SELECT * FROM [dbo].[staff]
WHERE [role] NOT IN ('Manager', 'Owner');

// 3. Searching Text (LIKE, NOT LIKE) //

SELECT * FROM [dbo].[guest]
WHERE [email] LIKE '%@email.com';

SELECT * FROM [dbo].[staff]
WHERE [staff_email] NOT LIKE 'mark%';

// 4. Handling Empty Values (IS NULL, IS NOT NULL) //

SELECT * FROM [dbo].[guest]
WHERE [phone] IS NULL;

SELECT * FROM [dbo].[payment]
WHERE [payment_method] IS NOT NULL;

// 5. Combining Logic (AND-OR) //

SELECT * FROM [dbo].[room]
WHERE [floor_number] = 1 
AND ([room_type] = 'Single' OR [room_type] = 'Double');
