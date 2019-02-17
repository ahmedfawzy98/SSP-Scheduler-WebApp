from scheduler.Classes.Schedule import Schedule


class Node:
	def __init__(self, data, sch=None):
		self.children = []
		self.parent = None
		self.data = data
		self.schedule = Schedule()
		if sch is not None:
			self.schedule.clone(sch)
		self.add_to_schedule()

	def add_child(self, data):
		child = Node(data, self.schedule)
		child.parent = self
		self.children.append(child)

	@staticmethod
	def check_clash(group, sch):
		if sch.checkClash(group.lecture):
			return True
		for i in range(len(group.tutorials)):
			if sch.checkClash(group.tutorials[i]):
				return True
		for i in range(len(group.labs)):
			if sch.checkClash(group.labs[i]):
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
		while current is not None:
			if not current.data.available:
				return False
			else:
				current = current.parent
		return True






