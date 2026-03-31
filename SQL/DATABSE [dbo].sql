CREATE TABLE [dbo].[guest] (
    [guest_Id]   INT           IDENTITY (1, 1) NOT NULL,
    [first_name] VARCHAR (50)  NOT NULL,
    [last_name]  VARCHAR (50)  NOT NULL,
    [email]      VARCHAR (100) NOT NULL,
    [phone]      VARCHAR (20)  NULL,
    CONSTRAINT [PK_guest] PRIMARY KEY CLUSTERED ([guest_Id] ASC),
    UNIQUE NONCLUSTERED ([email] ASC)
);


CREATE TABLE [dbo].[room] (
    [room_Id]         INT             IDENTITY (1, 1) NOT NULL,
    [room_number]     VARCHAR (10)    NOT NULL,
    [room_type]       VARCHAR (30)    NULL,
    [price_per_night] DECIMAL (10, 2) NULL,
    [floor_number]    INT             NULL,
    CONSTRAINT [PK_room] PRIMARY KEY CLUSTERED ([room_Id] ASC)
);


CREATE TABLE [dbo].[booking] (
    [booking_id]     INT             IDENTITY (1, 1) NOT NULL,
    [guest_id]       INT             NULL,
    [room_id]        INT             NULL,
    [check_in_date]  DATE            NOT NULL,
    [check_out_date] DATE            NOT NULL,
    [total_price]    DECIMAL (10, 2) NULL,
    CONSTRAINT [PK_booking] PRIMARY KEY CLUSTERED ([booking_id] ASC),
    FOREIGN KEY ([guest_id]) REFERENCES [dbo].[guest] ([guest_Id]),
    FOREIGN KEY ([room_id]) REFERENCES [dbo].[room] ([room_Id])
);


CREATE TABLE [dbo].[payment] (
    [payment_id]     INT             IDENTITY (1, 1) NOT NULL,
    [booking_id]     INT             NULL,
    [amount]         DECIMAL (10, 2) NULL,
    [payment_method] VARCHAR (50)    NULL,
    [payment_date]   DATE            NULL,
    CONSTRAINT [PK_payment] PRIMARY KEY CLUSTERED ([payment_id] ASC),
    FOREIGN KEY ([booking_id]) REFERENCES [dbo].[booking] ([booking_id])
);


CREATE TABLE [dbo].[staff] (
    [staff_id]    INT          IDENTITY (1, 1) NOT NULL,
    [first_name]  VARCHAR (50) NULL,
    [last_name]   VARCHAR (50) NULL,
    [role]        VARCHAR (50) NULL,
    [staff_email] VARCHAR (50) NULL,
    CONSTRAINT [PK_staff] PRIMARY KEY CLUSTERED ([staff_id] ASC),
    UNIQUE NONCLUSTERED ([staff_email] ASC)
);

