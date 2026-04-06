
import unittest
from pyvado import Pyvado, PyvadoError

class IntegrationTestPyvadoProcess(unittest.TestCase):

  def test_run_correct_command(self):

    proc = Pyvado("foo.xpr")

    proc.run_command("puts \"foo\"")

    self.assertTrue(True)

  def test_run_incorrect_command(self):

    proc = Pyvado("foo.xpr")

    with self.assertRaises(PyvadoError):
      proc.run_command("pust \"foo\"")


  def test_run_error_command(self):

    proc = Pyvado("foo.xpr")

    with self.assertRaises(PyvadoError):
      proc.run_command("launch_runs foo")
