from marshmallow import Schema, fields, pprint
import time

class ResponseSchema:
	def __init__(self,error=None, message = None, data=None, timestamp=None ):
		self.error = False
		self.message = ""
		self.data = {} if data==None else self.data
		self.timestamp = round(time.time())

	def customResponse(self, error, message, data=None):
		self.error = error 
		self.message = message
		self.data = data

	def successMessage(self, data=None):
		self.error = False
		self.message = "Operation completed Successfully"
		self.data = data

	def errorResponse(self, msg):
		self.error = True
		self.message = msg

	def __repr__(self): 
		return f'Error: {self.error}, Message: {self.message}, at: {self.timestamp}'

