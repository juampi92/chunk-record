import sounddevice as sd
import logging


class DeviceSelector:
    def cli_select(self):
        logging.info("Available audio devices:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            logging.info(
                f"{i}: {device['name']} (input channels: {device['max_input_channels']})"
            )

        device_index = int(input("Enter the device index you want to use: "))
        try:
            # Verifies if the selected device index is valid for input
            if sd.query_devices(device_index)["max_input_channels"] > 0:
                return device_index
            else:
                logging.info(
                    f"Device {device_index} does not support input. Please select another device."
                )
                return self.select_device()
        except Exception as e:
            logging.error(f"Error selecting device: {e}")
            return self.select_device()

    def select_by_name(self, device_name):
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            # Will check for a substring match
            if device["name"].lower().find(device_name.lower()) != -1:
                return i
        raise Exception(f"Device {device_name} not found.")

    # Will pick the first one that has `max_input_channels` > 0.
    def select_default(self):
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            # Will check for a substring match
            if device["max_input_channels"] > 0:
                logging.debug(f"Selected default device: {device['name']}")
                return i
        raise Exception(f"Default device not found. List: {devices}")
