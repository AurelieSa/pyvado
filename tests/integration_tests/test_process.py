
import unittest
from pyvado import PyvadoProcess, PyvadoError

class IntegrationTestPyvadoProcess(unittest.TestCase):

  def test_run_correct_command(self):

    proc = PyvadoProcess()

    proc.send("puts \"foo\"")

    self.assertTrue(True)

  def test_run_incorrect_command(self):

    proc = PyvadoProcess()

    with self.assertRaises(PyvadoError):
      proc.send("pust \"foo\"")

  def test_run_non_blocking_command(self):

    proc = PyvadoProcess()

    proc.send("puts \"foo\"", blocking = False)

    self.assertTrue(proc.read(), "foo\n")

  def test_run_error_command(self):

    proc = PyvadoProcess()

    with self.assertRaises(PyvadoError):
      proc.send("launch_runs foo")
