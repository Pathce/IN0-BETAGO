create table Test(
	No int NOT NULL primary key auto_increment,
    Reviewdate varchar(20) not null,
    Title varchar(30) not null,
    Review varchar(100) not null,
    Evaluation boolean not null
);