import CommandIntegrator as ci
import datetime
import pytz
import tzlocal

class Workshift:
	def __init__(self, timezone: pytz.timezone):
		self.timezone = timezone
		self.project = project = None
		self.end_timestamp: datetime.datetime = None
		self.start_timestamp: datetime.datetime = None
		self.break_minutes: int = None
		self.active: bool = False

	def __repr__(self):
		return f"Workshift object(project: {self.project}, duration: {self.duration})"

	@property
	def project(self):
		return self._project

	@project.setter
	def project(self, project: str):
		self._project = project

	@property
	def timezone(self):
		return self._timezone
	
	@timezone.setter
	def timezone(self, timezone: pytz.timezone):
		self._timezone = timezone

	@property
	def duration(self) -> dict:
		"""
		Calculate the duration of the workshift
		:returns:
			dict, containing worked hours and minutes,
			calculated as the time period between the 
			start and the end.
		"""
		minutes, hours = 0, 0
		
		if self.active:
			delta = (datetime.datetime.now(self.timezone) - self.start_timestamp)
		else:
			delta = (self.end_timestamp - self.start_timestamp)
		
		if (m := (delta.total_seconds() // 60)) >= 1: minutes = m
		while minutes >= 60:
			minutes -= 60
			hours += 1
		return {"hours": hours, "minutes": minutes}

	@property
	def date(self) -> str:
		if self.start_timestamp:
			return self.start_timestamp.strftime("%Y-%m-%d")
		return None

	@property
	def status(self) -> str:
		return "active" if self.active else "inactive"

	def start(self) -> None:
		"""
		Start the workshift clock.
		:returns:
			str, feedback that the workshift started
		"""
		if not self.active:
			self.start_timestamp = datetime.datetime.now(self.timezone)
			self.active = True

	def stop(self) -> None:
		"""
		Stop the workshift clock.
		:returns:
			str, feedback that the workshift stopeped
		"""
		if self.active:
			self.end_timestamp = datetime.datetime.now(self.timezone)
			self.active = False

class Logbook(dict):
	"""
	Collect Workshift instances and sort them by date.
	The object supports __getitem__ and __setitem__ which
	makes it easy to add and retrieve Workshift objects.
	"""
	def __init__(self):
		self.workshifts = {datetime.datetime.now().date(): list()}

	def __repr__(self):
		return f"Logbook object(logged days: {len([i for i in self.workshifts.keys()])})"

	def __str__(self):
		return f"Logbook({self.workshifts})"

	def __getitem__(self, date: datetime.datetime.date) -> list():
		"""
		Return the list with Workshifts that match the 
		date of recording.
		:param date:
			datetime.datetime.date instance, when the logs where
			recorded.
		:returns:
			list, containing Workshift instances if applicable
			else, None
		"""
		try:
			return self.workshifts[date]
		except KeyError:
			return None

	def append(self, workshift: Workshift, date = datetime.datetime.today().date()):
		try:
			self.workshifts[date].append(workshift)
		except KeyError:
			self.workshift[date] = [workshift]

	@property
	def timezone(self) -> pytz.timezone:
		return self._timezone

	@timezone.setter
	def timezone(self, timezone: pytz.timezone):
		self._timezone = timezone

class TimeKeeperFeature(ci.FeatureBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.active_workshift = None
		self.logbook = Logbook()
		self.timezone = tzlocal.get_localzone()
		self.command_parser = ci.CommandParser()
		self.command_parser.keywords = ("workshift", "workshifts", "work", "shift")
		self.command_parser.callbacks = {
			"on": self.log_on, "off": self.log_off, "list": self.get_shifts
		}
		self.command_parser.interactive_methods = (
			self.log_on, self.log_off
		)

	@ci.logger.loggedmethod
	def log_on(self, message: ci.Message) -> str:
		"""
		Create a new Workshift, set it as active.
		:returns:
			str
			phrase, indicating the start of a workshift.
		"""
		if not self.active_workshift:
			shift = Workshift(timezone = self.timezone)
			shift.start()
			self.active_workshift = shift
			return "Workshift started"
		return f"There is already an active workshift: {self.active_workshift}"

	@ci.logger.loggedmethod
	def log_off(self, message: ci.Message) -> str:
		"""
		Stop the current Workshift, and add it to the 
		logbook.
		:returns:
			str
			phrase, indicating the end of the most recent
			activated workshift, and its duration.
		"""
		if self.active_workshift:
			self.active_workshift.stop()
			self.logbook.append(self.active_workshift)
			duration = self.active_workshift.duration
			self.active_workshift = None
			return f"Workshift stopped. Logged time: {duration}"
		return "There are no active workshift to terminate."