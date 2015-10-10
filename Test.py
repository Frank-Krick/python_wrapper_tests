import unittest
import itk

class DeviceRegistryTest(unittest.TestCase):
    def test_device_registry_should_return_devices(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        print(devices)

class Test(unittest.TestCase):
    def test_test_test(self):
        self.assertTrue(1 == 2, "sucker")

testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(DeviceRegistryTest))
testSuite.addTest(unittest.makeSuite(Test))

if __name__ == "__main__":
    unittest.main()
