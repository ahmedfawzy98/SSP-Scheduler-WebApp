from scheduler.Classes import Schedule
class Node:
	def __init__(self,data,sch=None):
		self.children = []
		self.parent = None
		self.data = data
		self.schedule = Schedule()
		if(!sch):
			self.schedule.clone(sch)
		self.addToSchedule()



	def add_child(self,data):
		child = Node(data,self.getSchedule())
		child.parent=self
		self.children.append(child)


	def check_clash(self,group,sch):
		if(sch.checkClash(group.lecture)):
			return True
		for i in range(len(group.tutorials)):
			if(sch.checkClash(group.tutorials[i])):
				return True
		for i in range(len(group.labs)):
			if(sch.checkClash(group.labs[i])):
				return True
		return False


	def add_to_schedule(self):
		self.schedule.add_period(self.data.lecture)
		for i in range(len(self.data.tutorials)):
			self.schedule.add_period(self.data.tutorials[i])
		for i in range(len(self.data.labs)):
			self.schedule.add_period(self.data.labs[i])


	def all_available(self):
		current = self
		while(current!=None):
			if(!current.data.available):
				return False
			else:
				current = current.parent
		return True






