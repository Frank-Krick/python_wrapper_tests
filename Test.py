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
        device_graph = itk.DeviceGraph()
        node_id = device_graph.add_device(device)
        self.assertEqual(node_id, 0)
        device = registry.registeredDevices()[6]
        node_id = device_graph.add_device(device)
        self.assertEqual(node_id, 1)


class DeviceGraphConnectAudioDevice(unittest.TestCase):
    def test_connect_audio_devices(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        audio_devices = [device for device in devices if device.deviceType == itk.DeviceType.Audio]
        test_device = audio_devices[1]
        device_graph = itk.DeviceGraph()
        source = device_graph.add_device(test_device)
        target = device_graph.add_device(test_device)
        device_graph.connect(source, target)
        self.assertTrue(device_graph.is_connected(source, target))


class DeviceGraphConnectControlDevice(unittest.TestCase):
    def test_connect_control_devices(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        audio_devices = [device for device in devices if device.deviceType == itk.DeviceType.Audio]
        control_devices = [device for device in devices if device.deviceType == itk.DeviceType.Control]
        test_control_device = control_devices[0]
        test_audio_device = audio_devices[0]
        device_graph = itk.DeviceGraph()
        source = device_graph.add_device(test_control_device)
        target = device_graph.add_device(test_audio_device)
        device_graph.connect(source, target, 0)
        self.assertTrue(device_graph.is_connected(source, target, 0))


testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(DeviceRegistryTest))
testSuite.addTest(unittest.makeSuite(DeviceTypeTest))
testSuite.addTest(unittest.makeSuite(DeviceGraphConnectAudioDevice))
testSuite.addTest(unittest.makeSuite(DeviceGraphConnectControlDevice))


if __name__ == "__main__":
    unittest.main()
