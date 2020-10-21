import commandintegrator as ci
import discordInterface
import configparser as cp
from features.smarthomefeature import SmartHomeFeature

if __name__ == '__main__':

	config_parser = cp.ConfigParser()
	config_parser.read('config.ini')

	processor = ci.CommandProcessor()
	interface = discordInterface.discordInterface()

	processor.features = SmartHomeFeature()
	interface.command_processor = processor
	interface.guild = config_parser['DISCORD']['guild']

	interface.run(config_parser['DISCORD']['token'])