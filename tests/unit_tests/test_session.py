import unittest
from pyvado import PyvadoSession, PyvadoError
from pathlib import Path

class TestPyvadoSession(unittest.TestCase):

  def test_pyvado_session_path_empty(self):
    
    with self.assertRaises(ValueError):
      s = PyvadoSession(
        project_path = ""
      )

  def test_pyvado_session_wrong_extension(self):
    
    with self.assertRaises(ValueError):
      s = PyvadoSession(
        project_path = "foo/goo.xdc"
      )

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

    self.assertEqual(s.get_project_path(), pp)

  def test_pyvado_session_get_project_directory(self):

    pp = "foo/goo.xpr"

    s = PyvadoSession(
        project_path = pp
      )
    
    pp = Path(pp).resolve()

    self.assertEqual(s.get_project_dir(), pp.parent)

  def test_pyvado_session_get_project_name(self):

    pp = "foo/goo.xpr"

    s = PyvadoSession(
        project_path = pp
      )
    
    pp = Path(pp).resolve()

    self.assertEqual(s.get_project_name(), "goo")