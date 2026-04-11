import unittest
from pyvado import PyvadoSession, PyvadoError
from pathlib import Path

class TestPyvadoSession(unittest.TestCase):

  def test_pyvado_session_project_is_none_when_project_path_empty(self):

    pv = PyvadoSession()

    with self.assertRaises(PyvadoError):
      pv.project_path()

  def test_pyvado_session_wrong_extension(self):
    
    with self.assertRaises(ValueError):
      s = PyvadoSession(
        project_path = "foo/goo.xdc"
      )

  def test_pyvado_cant_open_porject_if_wrong_path(self):
     pv = PyvadoSession()

     with self.assertRaises(PyvadoError):
       pv.project.open()

  def test_pyvado_session_project_is_open_after_project_open(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.open_project()

    self.assertTrue(s.is_project_open())

  def test_pyvado_session_not_project_is_open_after_project_close(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.open_project()

    self.assertTrue(s.is_project_open())

    s.close_project()

    self.assertFalse(s.is_project_open())

  def test_pyvado_session_get_project_path(self):

    pp = "foo/goo.xpr"

    s = PyvadoSession(
        project_path = pp
      )
    
    pp = Path(pp).resolve()

    self.assertEqual(s.project_path, pp)

  def test_pyvado_session_get_project_directory(self):

    pp = "foo/goo.xpr"

    s = PyvadoSession(
        project_path = pp
      )
    
    pp = Path(pp).resolve()

    self.assertEqual(s.project_dir, pp.parent)

  def test_pyvado_session_get_project_name(self):

    pp = "foo/goo.xpr"

    s = PyvadoSession(
        project_path = pp
      )
    
    pp = Path(pp).resolve()

    self.assertEqual(s.project_name, "goo")

  def test_pyvado_session_hardware_is_open_after_hardware_open(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.open_hw()

    self.assertTrue(s.is_hw_open())

  def test_pyvado_session_not_hardware_is_open_after_hardware_close(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.open_hw()

    self.assertTrue(s.is_hw_open())

    s.close_hw()

    self.assertFalse(s.is_hw_open())

  def test_pyvado_session_hardware_target_is_open_after_hardware_target_open(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.open_target()

    self.assertTrue(s.is_target_open())

  def test_pyvado_session_not_hardware_target_is_open_after_hardware_target_close(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.open_target()

    self.assertTrue(s.is_target_open())

    s.close_target()

    self.assertFalse(s.is_target_open())

  def test_pyvado_session_hardware_server_is_open_after_hardware_server_open(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.connect_hw_server()

    self.assertTrue(s.is_hw_server_connected())

  def test_pyvado_session_not_hardware_target_is_open_after_hardware_target_close(self):

    s = PyvadoSession(
        project_path = "foo/goo.xpr"
      )
    
    s.connect_hw_server()

    self.assertTrue(s.is_hw_server_connected())

    s.disconnect_hw_server()

    self.assertFalse(s.is_hw_server_connected())