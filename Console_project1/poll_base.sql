CREATE TABLE Users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(50),
  age INT,
  login VARCHAR(50)
);

CREATE TABLE Polls (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) ,
  questions LONGTEXT
);

CREATE TABLE Results(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    answers LONGTEXT,
    answer_date DATE,
    poll_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (poll_id) REFERENCES Polls(id)
);