
from .entities.User import User
from werkzeug.security import generate_password_hash

from datetime import datetime

import os

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT * FROM users 
            WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
                        
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.contrasena),row[3], row[4], row[5], row[6], row[7])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def registerUser(self, db, user, password, mail,realname = "", country = "", profileimg = ""):
        try:
            cursor = db.connection.cursor()
            
            hashed_password = generate_password_hash(password)
            
            now = datetime.now()
            
            createdate = now.strftime("%Y%H%M%S")
            
            if profileimg != "":
                newprofileimg = createdate + profileimg.filename
                profileimg.save("src/static/Img/" + newprofileimg)
            else:
                newprofileimg = ""
            
            data = (user,hashed_password,realname,mail,country,now,newprofileimg)
            sql = "INSERT INTO users (id, username, contrasena, realname, mail, country, createdate, profileimg) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,data)
        
            sql2 = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            
            cursor.execute(sql2)
            
            row = cursor.fetchone() 
            
            
            db.connection.commit()
        
            return User(row[0],row[1],User.check_password(row[2], password),row[3],row[4],row[5],row[6],row[7])
        
        
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod    
    def checkAvailability(self, db, username):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT username FROM zcavengerdb.users WHERE username = '{}'".format(username))
            row = cursor.fetchone()
            if row != None:
                if row[0] == username:
                    return False
                else:
                    return True
            else:
                return True
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, id):
        """return a User() object by user id"""
        
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, realname, mail, country, createdate, profileimg FROM users WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3], row[4], row[5],row[6])
            else:
                print("No user found with id: " + id)
                return None
        except Exception as ex:
            raise Exception(ex)