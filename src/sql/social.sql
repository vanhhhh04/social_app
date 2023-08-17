DROP TABLE IF EXISTS social_app.message ;
DROP TABLE IF EXISTS social_app.notification  ;
DROP TABLE IF EXISTS social_app.favorited_nested_comments ;
DROP TABLE IF EXISTS social_app.favorited_comments ;
DROP TABLE IF EXISTS social_app.favorited_article ; 
DROP TABLE IF EXISTS social_app.nested_comment ;
DROP TABLE IF EXISTS social_app.comments ;
DROP TABLE IF EXISTS social_app.article ; 
DROP TABLE IF EXISTS social_app.user;

CREATE TABLE social_app.user (
    id SERIAL PRIMARY KEY , 
    name TEXT NOT NULL, 
    image TEXT ,
    bio  TEXT  , 
    username TEXT UNIQUE ,  
    password TEXT  
);
CREATE TABLE social_app.article (
    id SERIAL PRIMARY KEY ,
    title TEXT NOT NULL ,
		body TEXT ,
    created_at TIMESTAMP WITH TIME ZONE , 
    image TEXT ,
    id_author INT ,
    CONSTRAINT fk_user
    FOREIGN KEY(id_author) 
    REFERENCES social_app.user(id)
);
CREATE TABLE social_app.comments (
    id SERIAL PRIMARY KEY ,
    id_article INT ,
    id_user INT,
    body TEXT , 
    created_at TIMESTAMP WITH TIME ZONE ,
    CONSTRAINT fk_article 
    FOREIGN KEY (id_article) 
    REFERENCES social_app.article(id),
		CONSTRAINT fk_user
    FOREIGN KEY (id_user) 
    REFERENCES social_app.user(id)
);
CREATE TABLE social_app.nested_comment (
    id SERIAL PRIMARY KEY,
    id_big  INT,
    id_user INT, 
    id_article INT,
    body TEXT ,
    created_at TIMESTAMP WITH TIME ZONE ,
    CONSTRAINT fk_article
    FOREIGN KEY(id_article)
    REFERENCES social_app.article(id),
    CONSTRAINT fk_user 
    FOREIGN KEY(id_user)
    REFERENCES social_app.user(id),
    CONSTRAINT fk_comments 
    FOREIGN KEY(id_big)
    REFERENCES social_app.comments(id)
);
CREATE TABLE social_app.favorited_article (
    id_user INT ,
    id_article INT,
    id SERIAL PRIMARY KEY ,
    UNIQUE(id_user,id_article),
    CONSTRAINT fk_user 
    FOREIGN KEY (id_user)
    REFERENCES social_app.user(id),
    CONSTRAINT fk_article
    FOREIGN KEY (id_article) 
    REFERENCES social_app.article(id)
);
CREATE TABLE social_app.favorited_comments (
    id_comment INT ,
    id_user INT ,
    id SERIAL PRIMARY KEY ,
    UNIQUE (id_comment,id_user),
		CONSTRAINT fk_user 
    FOREIGN KEY (id_user)
    REFERENCES social_app.user(id),
		CONSTRAINT fk_comment 
    FOREIGN KEY (id_comment)
    REFERENCES social_app.comments(id)
		
);
CREATE TABLE social_app.favorited_nested_comments (
    id_nested_comment INT ,
    id_user INT ,
    id SERIAL PRIMARY KEY ,
    UNIQUE (id_nested_comment,id_user),
		CONSTRAINT fk_user 
    FOREIGN KEY (id_user)
    REFERENCES social_app.user(id),
		CONSTRAINT fk_nested_comment 
    FOREIGN KEY (id_nested_comment)
    REFERENCES social_app.nested_comment(id)
);
CREATE TABLE social_app.notification(
		id SERIAL PRIMARY KEY ,
		id_user INT ,
		id_new_cm INT ,
    id_new_nested_cm INT,
		id_new_fv_ar INT ,
		id_new_fv_cm INT ,
		id_new_fv_nested_cm INT ,
		created_at TIMESTAMP WITH TIME ZONE ,
		CONSTRAINT fk_user
		FOREIGN KEY (id_user)
		REFERENCES social_app.user(id),
		CONSTRAINT fk_comment
		FOREIGN KEY (id_new_cm)
		REFERENCES social_app.comments(id),
		CONSTRAINT fk_nested_comment 
    FOREIGN KEY (id_new_nested_cm)
    REFERENCES social_app.nested_comment(id),
    CONSTRAINT fk_article
		FOREIGN KEY (id_new_fv_ar)
		REFERENCES social_app.favorited_article(id),
		CONSTRAINT fk_comment1
		FOREIGN KEY (id_new_fv_cm)
		REFERENCES social_app.favorited_comments(id),
		CONSTRAINT fk_nested_comment2
		FOREIGN KEY (id_new_fv_nested_cm)
		REFERENCES social_app.favorited_nested_comments(id)
);
CREATE TABLE social_app.message(
	id SERIAL PRIMARY KEY ,
	id_author INT ,
	id_user INT ,
	CONSTRAINT fk_user 
	FOREIGN KEY (id_author) 
	REFERENCES social_app.user(id),
	CONSTRAINT fk_user1 
	FOREIGN KEY (id_user)
	REFERENCES social_app.user(id)
)