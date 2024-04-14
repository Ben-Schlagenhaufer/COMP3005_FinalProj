-- Create Members Table
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255), -- Should be hashed in a real-world application
    FitnessGoals TEXT,
    HealthMetrics TEXT
);

-- Create Trainers Table
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Expertise VARCHAR(255)
);

-- Create TrainerSchedule Table
CREATE TABLE TrainerSchedule (
    ScheduleID SERIAL PRIMARY KEY,
    TrainerID INT,
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID)
);

-- Create Administrative Staff Table
CREATE TABLE AdministrativeStaff (
    StaffID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Role VARCHAR(255),
    Email VARCHAR(255) UNIQUE -- Adding Email for uniformity and communication
);

-- Create Equipment Table
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    MaintenanceSchedule TEXT
);

-- Create Room Booking Table
CREATE TABLE RoomBookings (
    BookingID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255),
    BookingTime TIMESTAMP
);

-- Create Class Schedule Table
CREATE TABLE ClassSchedule (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255),
    TrainerID INT,
    StartTime TIMESTAMP,
    EndTime TIMESTAMP,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID)
);

-- Create Member Schedule Table
CREATE TABLE MemberSchedule (
    ScheduleID SERIAL PRIMARY KEY,
    MemberID INT,
    ClassID INT,
    BookingTime TIMESTAMP,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (ClassID) REFERENCES ClassSchedule(ClassID)
);

-- Create Billing Table
CREATE TABLE Billing (
    BillingID SERIAL PRIMARY KEY,
    MemberID INT,
    AmountDue NUMERIC(10, 2),
    DueDate TIMESTAMP,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);


-- Create MemberDashboard Table
CREATE TABLE MemberDashboard (
    EntryID SERIAL PRIMARY KEY,
    MemberID INT,
    Type VARCHAR(255),
    Description TEXT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);
