import CommandIntegrator as ci

class EchoFeature(ci.FeatureBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.command_parser = ci.CommandParser()
		self.command_parser.keywords = ("echo",)
		self.command_parser.callbacks = {"echo": self.echo}
		self.command_parser.interactive_methods = (self.echo,)

	@ci.logger.loggedmethod
	def echo(self, message: ci.Message) -> str:
		return f"You said {str(' ').join(message.content)}"