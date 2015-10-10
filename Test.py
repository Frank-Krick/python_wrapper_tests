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


class DeviceTypeTest(unittest.TestCase):
    def test_device_registry_should_return_devices_with_valid_device_types(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        for device in devices:
            self.assertTrue(device.deviceType == itk.DeviceType.Audio or
                            device.deviceType == itk.DeviceType.Control)


class DeviceGraphAddDevice(unittest.TestCase):
    def test_add_device_to_device_graph(self):
        registry = itk.DeviceRegistry()
        device = registry.registeredDevices()[3]
        device_graph = itk.DeviceGraph.create()
        node_id = device_graph.add_device(device)
        self.assertEqual(node_id, 0)
        device = registry.registeredDevices()[6]
        node_id = device_graph.add_device(device)
        self.assertEqual(node_id, 1)

testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(DeviceRegistryTest))
testSuite.addTest(unittest.makeSuite(DeviceTypeTest))

if __name__ == "__main__":
    unittest.main()
