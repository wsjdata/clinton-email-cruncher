#!/usr/bin/env python
# encoding: utf-8

from peewee import *
db = SqliteDatabase("hrcemail.sqlite")

class BaseModel(Model):
	class Meta:
		database = db

class Document(BaseModel):
	docID = CharField(max_length=9,unique=True,primary_key=True)
	subject = CharField(null=True)
	documentClass = CharField()
	pdfLink = CharField()
	originalLink = CharField(null=True)
	docDate = DateField(null=True)
	postedDate = DateField()
	#from is a reserved word
	messageFrom = CharField(db_column="from",null=True)
	to = CharField(null=True)
	messageNumber = CharField(null=True)
	caseNumber = CharField()
	docText = TextField(null=True)
		
class Name(BaseModel):
	originalName = CharField(primary_key=True)
	commonName = CharField()

db.connect()
#create tables if they don't exist
db.create_tables([Document,Name],True)