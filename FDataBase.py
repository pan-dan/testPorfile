import sqlite3
import time
import math
import re
from flask import url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False

            base = url_for('static', filename='img')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>",
                          text)

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return []

    def addUser(self, login, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as count FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print ("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            standartBlog = "Здесь будет информация о себе, которую заполняли ранее или будет возможность нажать сюда и написать всё, что нужно"
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, ?, ?)", (login, email, hpsw, standartBlog, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД" + str(e))
            return False

        return True


    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошиибка получения данных из БД " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

    def updateUserInformation(self, user_id, first_name, last_name, country, city, blog):
        if not (first_name and last_name and country and city and blog):
            return False

        try:
            query = "UPDATE users SET "
            params = []

            if first_name:
                query += "first_name = ?, "
                params.append(first_name)
            if last_name:
                query += "last_name = ?, "
                params.append(last_name)
            if country:
                query += "country = ?, "
                params.append(country)
            if city:
                query += "city = ?, "
                params.append(city)
            if blog:
                query += "blog = ?, "
                params.append(blog)

            query = query.rstrip(", ")  # Удаляем лишнюю запятую и пробел в конце строки
            query += " WHERE id = ?"
            params.append(user_id)

            self.__cur.execute(query, tuple(params))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления информации о пользователе в БД: " + str(e))
            return False
        return True
        #     В этой версии кода мы создаем строку запроса query, которая будет динамически формироваться в зависимости от
        # того, какие переменные имеют новые значения.Переменные, которым присваивается новое значение, добавляются в
        # строку запроса и соответствующее значение добавляется в список params. \
        #     После построения запроса мы удаляем лишнюю запятую и пробел в конце строки запроса с помощью rstrip(", ").
        #     Затем мы добавляем значение user_id в список params и выполняем запрос с использованием execute(),
        # передавая кортеж params в качестве параметров.
        #     Теперь, если какие - то переменные(first_name, last_name, country, city) остаются пустыми или не имеют новых
        # значений, они не будут включены в запрос обновления, и соответствующие столбцы в базе данных сохранят свои
        # предыдущие значения.

    def getBlog(self, user_id):
        try:
            self.__cur.execute(f"SELECT blog FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res[0]
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД: " + str(e))
        return False
