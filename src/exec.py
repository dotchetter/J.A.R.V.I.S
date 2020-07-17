import CommandIntegrator as ci
import discordInterface
import configparser as cp
from features.echofeature import EchoFeature
from features.timekeeperfeature import TimeKeeperFeature

if __name__ == '__main__':

	config_parser = cp.ConfigParser()
	config_parser.read('config.ini')

	echo = EchoFeature()
	timekeeper = TimeKeeperFeature()

	processor = ci.CommandProcessor()
	interface = discordInterface.discordInterface()

	processor.features = (echo, timekeeper)
	interface.command_processor = processor
	interface.guild = config_parser['DISCORD']['guild']

	interface.run(config_parser['DISCORD']['token'])