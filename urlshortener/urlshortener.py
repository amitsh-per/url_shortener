from os.path import isfile
from sys import implementation
from flask import Flask, render_template, request, redirect
from markupsafe import escape
from abc import ABC, abstractmethod
import pickle, shortuuid
import os, pdb

class UrlDb:
    def __init__(self):
        self._max_rows_added_since_last_save=1
        self._rows_added_since_last_save=0
    @abstractmethod
    def getLong():
        pass
    @abstractmethod
    def save(self):
        pass

class UrlSqlDb(UrlDb):
    @abstractmethod
    def getLong(self):
        pass
    @abstractmethod
    def save(self):
        pass
    @abstractmethod
    def createCache():
        pass

class UrSqlitelDb(UrlSqlDb):
    def getLong(self):
        pass
    def save(self):
        pass
    def createCache():
        pass

class UrlNoSqlDb(UrlDb):
    @abstractmethod
    def getLong(self):
        pass
    @abstractmethod
    def save(self):
        pass
    @abstractmethod
    def createCache():
        pass

class UrlCassandraDb(UrlNoSqlDb):
    def getLong(self):
        pass
    def save(self):
        pass
    def createCache():
        pass

class UrlShelveDb(UrlNoSqlDb):
    def getLong(self):
        pass
    def save(self):
        pass
    def createCache():
        pass

class UrlPickleDb(UrlDb):

    def __init__(self):
        UrlDb.__init__(self)
        if isfile('db.pickle'):
            pickle_file=open('db.pickle', 'rb')
            self._db=pickle.load(pickle_file)
            pickle_file.close()
        else:
            self._db = dict()

    def getLong(self,short):
        return self._db.get(short, '')

    def save(self, short, long):
        old_long=self._db.get(short, None) 
        if old_long is not None and old_long != long :
            #Collision
            return False
        else:
            self._db[short]=long
            self._rows_added_since_last_save+=1
            self.__save_to_disk()
        return True

    def __save_to_disk(self):
        if self._rows_added_since_last_save>=self._max_rows_added_since_last_save:
            pickle_file=open('db.pickle', 'wb')
            pickle.dump(self._db, pickle_file)
            self._rows_added_since_last_save=0
            pickle_file.close()

class UrlManager():
    
    def __init__(self):
        self._urlDbObj=UrlPickleDb()
    
    def getLong(self, short):
        return self._urlDbObj.getLong(short)
    
    def getShort(self, long):
        id=shortuuid.uuid(name=long)
        short=id[:7]
        if self._urlDbObj.save(short,long):
            return short
        else:
            return "INTERNAL_EXCEPTION: Collision with another URL. Please try a different URL" 
   
app = Flask(__name__)    
url_manager=UrlManager()
@app.route("/u/<short>")
def redirect_to_long(short):
    short=escape(short)
    #redirect to long url here
    long=url_manager.getLong(short)
    if long != '' and long is not None:
        return redirect(long, code="302")
    else:
        return f"<p>Web address: http://127.0.0.1:5000/u/{escape(short)}  not found. Please enter the correct shortened URL in address bar of the browser</p>"

@app.route('/')
def my_form():
    return render_template('my-form.html.jinja')

@app.route('/', methods=['POST'])
def my_form_post():
    long = request.form['long']
    short_url=url_manager.getShort(long)
    return "\n Please note down your shortened URL. Enter it in a browser address bar to access your website and bookmark it. ---> http://127.0.0.1:5000/u/" + short_url

