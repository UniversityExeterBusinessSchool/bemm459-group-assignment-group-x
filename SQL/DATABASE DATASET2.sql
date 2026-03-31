
INSERT INTO [dbo].[guest] ([first_name], [last_name], [email], [phone])
VALUES 
('Liam', 'Smith', 'liam.s@email.com', '555-0101'), ('Emma', 'Johnson', 'emma.j@email.com', '555-0102'),
('Noah', 'Williams', 'noah.w@email.com', '555-0103'), ('Olivia', 'Brown', 'olivia.b@email.com', '555-0104'),
('William', 'Jones', 'will.j@email.com', '555-0105'), ('Sophia', 'Garcia', 'sophia.g@email.com', '555-0106'),
('James', 'Miller', 'james.m@email.com', '555-0107'), ('Isabella', 'Davis', 'isabella.d@email.com', '555-0108'),
('Benjamin', 'Rodriguez', 'ben.r@email.com', '555-0109'), ('Charlotte', 'Martinez', 'char.m@email.com', '555-0110'),
('Lucas', 'Hernandez', 'lucas.h@email.com', '555-0111'), ('Mia', 'Lopez', 'mia.l@email.com', '555-0112'),
('Henry', 'Gonzalez', 'henry.g@email.com', '555-0113'), ('Amelia', 'Wilson', 'amelia.w@email.com', '555-0114'),
('Alexander', 'Anderson', 'alex.a@email.com', '555-0115'), ('Evelyn', 'Thomas', 'evelyn.t@email.com', '555-0116'),
('Michael', 'Taylor', 'mike.t@email.com', '555-0117'), ('Abigail', 'Moore', 'abby.m@email.com', '555-0118'),
('Daniel', 'Jackson', 'dan.j@email.com', '555-0119'), ('Elizabeth', 'Martin', 'eliz.m@email.com', '555-0120');



INSERT INTO [dbo].[room] ([room_number], [room_type], [price_per_night], [floor_number])
VALUES 
('101', 'Single', 100.00, 1), ('102', 'Single', 100.00, 1), ('103', 'Double', 150.00, 1), ('104', 'Double', 150.00, 1),
('201', 'Single', 110.00, 2), ('202', 'Single', 110.00, 2), ('203', 'Double', 160.00, 2), ('204', 'Double', 160.00, 2),
('301', 'Single', 120.00, 3), ('302', 'Single', 120.00, 3), ('303', 'Double', 170.00, 3), ('304', 'Double', 170.00, 3),
('401', 'Suite', 300.00, 4), ('402', 'Suite', 300.00, 4), ('403', 'Suite', 300.00, 4), ('404', 'Suite', 300.00, 4),
('501', 'Penthouse', 1000.00, 5), ('502', 'Penthouse', 1000.00, 5), ('503', 'Penthouse', 1000.00, 5), ('504', 'Penthouse', 1000.00, 5);



INSERT INTO [dbo].[booking] ([guest_id], [room_id], [check_in_date], [check_out_date], [total_price])
VALUES 
(1, 1, '2026-05-01', '2026-05-03', 200.00), (2, 2, '2026-05-01', '2026-05-04', 300.00),
(3, 3, '2026-05-02', '2026-05-05', 450.00), (4, 4, '2026-05-03', '2026-05-04', 150.00),
(5, 5, '2026-05-05', '2026-05-06', 110.00), (6, 6, '2026-05-06', '2026-05-08', 220.00),
(7, 7, '2026-05-07', '2026-05-09', 320.00), (8, 8, '2026-05-08', '2026-05-11', 480.00),
(9, 9, '2026-05-10', '2026-05-12', 240.00), (10, 10, '2026-05-11', '2026-05-15', 480.00),
(11, 11, '2026-05-12', '2026-05-14', 340.00), (12, 12, '2026-05-13', '2026-05-15', 340.00),
(13, 13, '2026-05-14', '2026-05-17', 900.00), (14, 14, '2026-05-15', '2026-05-16', 300.00),
(15, 15, '2026-05-16', '2026-05-20', 1200.00), (16, 16, '2026-05-17', '2026-05-19', 600.00),
(17, 17, '2026-05-18', '2026-05-21', 3000.00), (18, 18, '2026-05-19', '2026-05-22', 3000.00),
(19, 19, '2026-05-20', '2026-05-22', 2000.00), (20, 20, '2026-05-21', '2026-05-23', 2000.00);



INSERT INTO [dbo].[payment] ([booking_id], [amount], [payment_method], [payment_date])
VALUES 
(1, 200.00, 'Cash', '2026-05-01'), (2, 300.00, 'Credit Card', '2026-05-01'),
(3, 450.00, 'Debit Card', '2026-05-02'), (4, 150.00, 'Cash', '2026-05-03'),
(5, 110.00, 'Credit Card', '2026-05-05'), (6, 220.00, 'Credit Card', '2026-05-06'),
(7, 320.00, 'Cash', '2026-05-07'), (8, 480.00, 'Debit Card', '2026-05-08'),
(9, 240.00, 'Credit Card', '2026-05-10'), (10, 480.00, 'Credit Card', '2026-05-11'),
(11, 340.00, 'Cash', '2026-05-12'), (12, 340.00, 'Debit Card', '2026-05-13'),
(13, 900.00, 'Credit Card', '2026-05-14'), (14, 300.00, 'Cash', '2026-05-15'),
(15, 1200.00, 'Credit Card', '2026-05-16'), (16, 600.00, 'Debit Card', '2026-05-17'),
(17, 3000.00, 'Credit Card', '2026-05-18'), (18, 3000.00, 'Cash', '2026-05-19'),
(19, 2000.00, 'Credit Card', '2026-05-20'), (20, 2000.00, 'Debit Card', '2026-05-21');



INSERT INTO [dbo].[staff] ([first_name], [last_name], [role], [staff_email])
VALUES 
('James', 'Bond', 'Security', 'j.bond@hotel.com'), ('Sarah', 'Connor', 'Manager', 's.connor@hotel.com'),
('Ellen', 'Ripley', 'Housekeeping', 'e.ripley@hotel.com'), ('Tony', 'Stark', 'Maintenance', 't.stark@hotel.com'),
('Bruce', 'Wayne', 'Owner', 'b.wayne@hotel.com'), ('Diana', 'Prince', 'Reception', 'd.prince@hotel.com'),
('Clark', 'Kent', 'Concierge', 'c.kent@hotel.com'), ('Barry', 'Allen', 'Room Service', 'b.allen@hotel.com'),
('Hal', 'Jordan', 'Security', 'h.jordan@hotel.com'), ('Arthur', 'Curry', 'Pool Manager', 'a.curry@hotel.com');
