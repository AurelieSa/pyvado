
import unittest
from pyvado import Pyvado, PyvadoError

class IntegrationTestPyvadoProcess(unittest.TestCase):

  def test_run_correct_command(self):

    proc = Pyvado()

    proc.tcl.run("puts \"foo\"")

    self.assertTrue(True)

  def test_run_incorrect_command(self):

    proc = Pyvado("foo.xpr")

    with self.assertRaises(PyvadoError):
      proc.tcl.run("pust \"foo\"")


  def test_run_error_command(self):

    proc = Pyvado()

    with self.assertRaises(PyvadoError):
      proc.tcl.run("launch_runs foo")
