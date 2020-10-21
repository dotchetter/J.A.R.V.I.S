import commandintegrator as ci
import serial


class SmartHomeFeature(ci.FeatureBase):
    """
    Communicate with various devices in the home.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial_communicator = None
        self.command_parser = ci.CommandParser(keywords="alarm")
        self.command_parser.callbacks = (
            ci.Callback(lead=("engage", "on"), func=self.engage_alarm),
            ci.Callback(lead=("disengage", "off"), func=self.disengage_alarm))
        self.assign_serial_communicator()

    def assign_serial_communicator(self):
        """
        Iterate over the port 0 - 10 and try to connect
        with it over UART. Primitive, but works for now.
        """
        for i in range(10):
            try:
                self.serial_communicator = serial.Serial(port=f"COM{i}",
                                                         baudrate=38400)
            except serial.serialutil.SerialException:
                pass

    @ci.logger.loggedmethod
    def engage_alarm(self) -> str:
        self.serial_communicator.write(b"ON")
        return "Alarm activated"

    @ci.logger.loggedmethod
    def disengage_alarm(self) -> str:
        self.serial_communicator.write(b"OFF")
        return "Alarm deactivated"
