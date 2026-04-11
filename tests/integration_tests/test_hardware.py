
import unittest
from pyvado import Pyvado, PyvadoError
from os import listdir 

class IntegrationTestHardwareManager(unittest.TestCase):

  def test_program_device_steps_default(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    bitstream_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1/toplevel_test.bit"

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.synthesis()

    pv.flow.implementation()

    pv.flow.bitstream()

    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()
    pv.hardware.set_bitstream(bitstream_path)
    pv.hardware.program_device()

  def test_program_device_steps_find_bitstream_file(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.synthesis()

    pv.flow.implementation()

    pv.flow.bitstream()

    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()
    pv.hardware.set_bitstream()
    pv.hardware.program_device()

  def test_program_device_steps_project_close(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    bitstream_path = "./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1/toplevel_test.bit"

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.synthesis()

    pv.flow.implementation()

    pv.flow.bitstream()

    pv.project.close()

    pv.hardware.open_hardware()
    pv.hardware.connect_server()
    pv.hardware.open_target()
    pv.hardware.set_bitstream(bitstream_path)
    pv.hardware.program_device()

  def test_deploy(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.synthesis()

    pv.flow.implementation()

    pv.flow.bitstream()

    pv.hardware.deploy()