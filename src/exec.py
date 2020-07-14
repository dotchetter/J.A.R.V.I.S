import CommandIntegrator as ci
import discordInterface
import configparser as cp
from features.echofeature import EchoFeature

if __name__ == '__main__':

	config_parser = cp.ConfigParser()
	config_parser.read('config.ini')

	echo_feature = EchoFeature()

	processor = ci.CommandProcessor()
	interface = discordInterface.discordInterface()

	processor.features = echo_feature
	interface.command_processor = processor
	interface.guild = config_parser['DISCORD']['guild']

	interface.run(config_parser['DISCORD']['token'])