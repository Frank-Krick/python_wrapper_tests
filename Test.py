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


class DeviceGraphDescribeDevices(unittest.TestCase):
    def test_device_graph_describes_included_devices(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        device_graph = itk.DeviceGraph()
        for device in devices:
            device.id = device_graph.add_device(device)
        self.assertEqual(len(device_graph.devices), len(devices))
        device_ids_one = map(lambda x: x.id, devices)
        device_ids_one.sort()
        device_ids_two = map(lambda x: x.deviceId, device_graph.devices)
        device_ids_two.sort()
        self.assertEqual(device_ids_one, device_ids_two)


class DeviceGraphReturnConnections(unittest.TestCase):
    def test_device_graph_should_return_connections(self):
        registry = itk.DeviceRegistry()
        devices = registry.registeredDevices()
        audio_devices = [device for device in devices if device.deviceType == itk.DeviceType.Audio]
        control_devices = [device for device in devices if device.deviceType == itk.DeviceType.Control]
        audio_device = audio_devices[0]
        control_device = control_devices[0]
        device_graph = itk.DeviceGraph()
        audio_device_ids = [
            device_graph.add_device(audio_device),
            device_graph.add_device(audio_device),
            device_graph.add_device(audio_device),
            device_graph.add_device(audio_device),
            device_graph.add_device(audio_device),
        ]
        control_device_ids = [
            device_graph.add_device(control_device),
            device_graph.add_device(control_device),
            device_graph.add_device(control_device),
            device_graph.add_device(control_device),
            device_graph.add_device(control_device),
        ]
        expected_control = [
            (control_device_ids[0], audio_device_ids[0], 0),
            (control_device_ids[1], audio_device_ids[1], 0),
            (control_device_ids[2], audio_device_ids[2], 0),
            (control_device_ids[1], audio_device_ids[3], 0),
            (control_device_ids[2], audio_device_ids[2], 0),
            (control_device_ids[3], audio_device_ids[3], 0),
        ]
        for edge in expected_control:
            device_graph.connect(edge[0], edge[1], edge[2])
        expected_audio = [
            (audio_device_ids[0], audio_device_ids[1]),
            (audio_device_ids[1], audio_device_ids[2]),
            (audio_device_ids[0], audio_device_ids[3]),
            (audio_device_ids[3], audio_device_ids[2]),
            (audio_device_ids[3], audio_device_ids[4]),
        ]
        for edge in expected_audio:
            device_graph.connect(edge[0], edge[1])
        actual_return_audio = device_graph.audioConnections
        actual_audio = map(lambda x: (x.source, x.target), actual_return_audio)
        actual_audio.sort()
        expected_audio.sort()
        self.assertEqual(actual_audio, expected_audio)
        actual_return_control = device_graph.controlConnections
        actual_control = map(lambda x: (x.source, x.target, x.parameter), actual_return_control)
        actual_control.sort()
        expected_control.sort()
        self.assertEqual(expected_control, actual_control)


testSuite = unittest.TestSuite()
testSuite.addTest(unittest.makeSuite(DeviceRegistryTest))
testSuite.addTest(unittest.makeSuite(DeviceTypeTest))
testSuite.addTest(unittest.makeSuite(DeviceGraphConnectAudioDevice))
testSuite.addTest(unittest.makeSuite(DeviceGraphConnectControlDevice))
testSuite.addTest(unittest.makeSuite(DeviceGraphDescribeDevices))
testSuite.addTest(unittest.makeSuite(DeviceGraphReturnConnections))

if __name__ == "__main__":
    unittest.main()
