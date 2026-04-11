import unittest
from pyvado import Pyvado, PyvadoError
from os import listdir 

class IntegrationTestPyvadoFlow(unittest.TestCase):

  def test_reset_synth_remove_runs(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    synth_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/synth_1")

    self.assertEqual(len(synth_dir), 0)

    with self.assertRaises(FileNotFoundError):
      impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")


  def test_synth_flow(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")
  
    pv.flow.synthesis()

    synth_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/synth_1")

    self.assertNotEqual(len(synth_dir), 0)

  def test_impl_after_synth_flow(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.synthesis()

    pv.flow.implementation()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertNotEqual(len(impl_dir), 0)

  def test_run_impl_also_run_synth(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )
    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.implementation()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")
    synth_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/synth_1")

    self.assertNotEqual(len(synth_dir), 0)
    self.assertNotEqual(len(impl_dir), 0)

  def test_bitstream_flow_after_impl(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.implementation()

    pv.flow.bitstream()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertTrue((any(f.endswith(".bit") for f in impl_dir)))

  def test_run_bitstream_also_run_impl_and_synth(self):
    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.bitstream()

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertTrue((any(f.endswith(".bit") for f in impl_dir)))

  def test_reset_impl_onyl_remove_impl(self):

    pv = Pyvado(
      project_path="./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.xpr"
    )

    pv.project.open()

    pv.flow.reset_run(run_name="synth_1")

    pv.flow.implementation()

    pv.flow.reset_run(run_name="impl_1")

    impl_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/impl_1")

    self.assertEqual(len(impl_dir), 2)

    synth_dir = listdir("./tests/integration_tests/pyvado_integration_test_project/pyvado_integration_test_project.runs/synth_1")
    self.assertNotEqual(len(synth_dir), 0)
