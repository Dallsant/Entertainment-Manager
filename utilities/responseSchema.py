from marshmallow import Schema, fields, pprint
import time

class ResponseSchema:
	def __init__(self,error=None, message = None, data=None, timestamp=None ):
		self.error = False
		self.message = ""
		self.data = {} if data==None else self.data
		self.timestamp = time.time()

	def customResponse(self, error, message):
		self.error = error 
		self.message = message

	def successResponse(self):
		self.error = false
		self.message = "Operation completed Successfully"

	def errorResponse(self, msg ):
		self.error = true
		self.message = msg

	def __repr__(self): 
		return f'Error: {self.error}, Message: {self.message}, at: {self.timestamp}'

# response = ResponseObject()
# print(response)