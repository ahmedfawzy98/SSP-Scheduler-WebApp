class Schedule:
	def __init__(self):
		self.schedule = [
						[0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0]
						]
		self.input = None
		self.days = [False,False,False,False,False,False]
		self.daysTaken = 0
		self.priorityValue = 0


	def check_clash(self,period):
		for i in range(period.length):
			if(self.schedule[period.time.day][period.time.fr+i] != 0):
				return True
		return False


	def add_period(self,period):
		for i in range(period.length):
			self.schedule[period.time.day][period.time.fr+i] = period
		if(self.days[period.time.day] == False):
			self.daysTaken+=1
			self.days[period.time.day] = True

	def add_to_priority(self,value):
		self.priority = self.priority+value

	def clone(self, sch):
		for i in range(6):
			for j in range(12):
				self.schedule[i][j] = sch.schedule[i][j]

		self.priorityValue = sch.priorityValue
		self.daysTaken = sch.daysTaken
		for i in range(6):
			self.days[i] = sch.days[i]