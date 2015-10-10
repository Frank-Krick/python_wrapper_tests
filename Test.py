import unittest
import itk


class DeviceRegistryTest(unittest.TestCase):
    def test_device_registry_should_return_at_least_one_valid_device(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        self.assertGreater(len(devices), 0)
        device = devices[6]
        self.assertIsNotNone(device.name)
        self.assertNotEqual(device.description, "")


testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(DeviceRegistryTest))

if __name__ == "__main__":
    unittest.main()
