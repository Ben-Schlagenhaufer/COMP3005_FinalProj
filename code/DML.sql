-- Populate the Members Table
INSERT INTO Members (FirstName, LastName, Email, Password, FitnessGoals, HealthMetrics)
VALUES 
('John', 'Doe', 'john.doe@example.com', 'hashed_password1', 'Lose weight', 'None'),
('Jane', 'Smith', 'jane.smith@example.com', 'hashed_password2', 'Increase strength', 'Good'),
('Alice', 'Wong', 'alice.wong@example.com', 'hashed_password3', 'Run a marathon', 'Excellent'),
('Bob', 'Marley', 'bob.marley@example.com', 'hashed_password4', 'Improve flexibility', 'Poor');

-- Populate the Trainers Table
INSERT INTO Trainers (FirstName, LastName, Email, Expertise)
VALUES 
('Alice', 'Johnson', 'alice.johnson@example.com', 'Yoga'),
('Bob', 'Brown', 'bob.brown@example.com', 'Weightlifting'),
('Charlie', 'Black', 'charlie.black@example.com', 'Pilates'),
('Diana', 'White', 'diana.white@example.com', 'Cardio Fitness');

-- Populate the TrainerSchedule Table
INSERT INTO TrainerSchedule (TrainerID, StartTime, EndTime)
VALUES 
(1, '2024-06-02 08:00:00', '2024-06-02 12:00:00'),
(1, '2024-06-04 14:00:00', '2024-06-04 18:00:00'),
(2, '2024-06-03 09:00:00', '2024-06-03 13:00:00'),
(3, '2024-06-05 10:00:00', '2024-06-05 14:00:00'),
(4, '2024-06-06 16:00:00', '2024-06-06 20:00:00');

-- Populate the MemberDashboard Table with sample data
INSERT INTO MemberDashboard (MemberID, Type, Description)
VALUES 
(1, 'Exercise Routines', 'Running 5km daily'),
(1, 'Exercise Routines', 'Cycling 10km on weekends'),
(1, 'Fitness Achievements', 'Completed first marathon'),
(1, 'Fitness Achievements', 'Achieved personal best in deadlift'),
(1, 'Health Statistics', 'Resting Heart Rate: 60bpm'),
(1, 'Health Statistics', 'Body Fat: 20%'),
(2, 'Exercise Routines', 'Sun Salutation series for flexibility'),
(2, 'Exercise Routines', 'Meditation for relaxation'),
(2, 'Fitness Achievements', 'Mastered the Crow Pose'),
(2, 'Fitness Achievements', '30 consecutive days of Yoga practice'),
(2, 'Health Statistics', 'Improved flexibility'),
(2, 'Health Statistics', 'Reduced stress levels');

-- Populate the Equipment Table
INSERT INTO Equipment (Name, MaintenanceSchedule)
VALUES 
('Treadmill', 'Every 6 months'),
('Dumbbell Set', 'Annually');

-- Populate the Room Bookings Table
INSERT INTO RoomBookings (RoomName, BookingTime)
VALUES 
('Aerobics Room', '2024-05-15 10:00:00'),
('Spinning Room', '2024-05-16 12:00:00');

-- Populate the Class Schedule Table
INSERT INTO ClassSchedule (ClassName, TrainerID, StartTime, EndTime)
VALUES 
('Beginner Yoga', 1, '2024-06-01 10:00:00', '2024-06-01 11:00:00'),
('Advanced Weightlifting', 2, '2024-06-01 15:00:00', '2024-06-01 16:30:00'),
('Intermediate Pilates', 3, '2024-06-02 09:00:00', '2024-06-02 10:30:00'),
('High Intensity Cardio', 4, '2024-06-02 14:00:00', '2024-06-02 15:30:00');

-- Populate the Member Schedule Table
INSERT INTO MemberSchedule (MemberID, ClassID, BookingTime)
VALUES 
(1, 1, '2024-06-01 10:00:00'),
(2, 2, '2024-06-01 15:00:00'),
(3, 3, '2024-06-02 09:00:00'),
(4, 4, '2024-06-02 14:00:00');

INSERT INTO AdministrativeStaff (FirstName, LastName, Role, Email)
VALUES ('Rob', 'Ford', 'Admin', 'rob.ford@example.com');

-- Populate the Billing Table
INSERT INTO Billing (MemberID, AmountDue, DueDate)
VALUES 
(1, 100.00, '2024-07-01'),
(2, 150.50, '2024-07-15'),
(3, 75.25, '2024-07-20'),
(4, 200.00, '2024-07-25');
