create table Test(
	No int NOT NULL primary key auto_increment,
    Reviewdate varchar(20) not null,
    Title varchar(30) not null,
    Review varchar(100) not null,
    Evaluation boolean not null
);

insert into Test(Reviewdate, Title, Review, Evaluation)
values
("20210401", "너의 이름은", "재밌어요", True),
("20210411", "신과 함께", "재미없어요", False),
("20210420", "너의 이름은", "노잼", False),
("20210511", "분노의 질주: 더 얼티메이트", "", True),
("20210520", "분노의 질주: 더 얼티메이트", "굿", True),
("20210521", "캐인 인 더 우즈", "", False);