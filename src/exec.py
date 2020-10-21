import argparse
import configparser as cp

import commandintegrator as ci
import discordInterface
from features.smarthomefeature import SmartHomeFeature

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", action="store_true")

    args = parser.parse_args()

    config_parser = cp.ConfigParser()
    config_parser.read('config.ini')

    processor = ci.CommandProcessor()
    interface = discordInterface.discordInterface()

    processor.features = SmartHomeFeature()
    interface.command_processor = processor
    interface.guild = config_parser['DISCORD']['guild']

    if args.debug:

        import speech_recognition as sr
        r = sr.Recognizer()
        message = ci.Message()

        print("J.A.R.V.I.S debug console",
              "Version: 0.2.4 A\n\n",
              f"Features loaded: {[i for i in processor.features]}",
              "\n -> JARVIS is ready.", sep="\n")

        while True:
            with sr.Microphone() as source:
                audio = r.listen(source)

                try:
                    recognized = r.recognize_google(audio)
                except sr.UnknownValueError:
                    continue

                print("You:", recognized)
                message.content = recognized

            response = processor.process(message)
            print(f"\nJarvis: {response.response()}")

    else:
        interface.run(config_parser['DISCORD']['token'])