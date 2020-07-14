import CommandIntegrator as ci
import discord
import asyncio

class discordInterface(discord.Client):
	"""
	Client class to integrate with the Discord API
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for key, value in kwargs.items():
			setattr(self, key, value)

	@property
	def command_processor(self):
		return self._command_processor
	
	@command_processor.setter
	def command_processor(self, processor: ci.CommandProcessor):
		self._command_processor = processor

	@property
	def guild(self):
		return self._guild

	@guild.setter
	def guild(self, guild: str) -> str:
		self._guild = guild

	@ci.logger.loggedmethod
	async def on_message(self, message: discord.Message) -> str:
		"""
		Process message read from discord, either through
		pm or in one of the channels.
		:param message:
			discord.Message
			Incoming message object for processing
		:returns:
			str
			processed response			
		"""
		if message.author != self.user:
			processed = self._command_processor.process(message)
			if processed: await message.channel.send(processed.response())