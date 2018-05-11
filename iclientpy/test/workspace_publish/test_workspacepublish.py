from unittest import TestCase, mock
from iclientpy.codingui.servicepublish import PrepareWorkspacePublish


class WorkspacePublishTestCase(TestCase):
    def test_file_workspace(self):
        post_func = mock.MagicMock()
        wsp = PrepareWorkspacePublish(post_func)
        wsp.use_file_workspace()
        self.assertTrue(hasattr(wsp.workspace, 'set_path'))
        wsp.workspace.set_path('test')
        wsp.allow_edit()
        wsp.avaliable_service_types.RESTDATA.select()
        wsp.avaliable_service_types.RESTDATA.remove()
        wsp.avaliable_service_types.RESTMAP.select()
        wsp.execute()
        self.assertEqual(str(wsp), """{
  "isDataEditable": true,
  "servicesTypes": [
    "RESTMAP"
  ],
  "workspaceConnectionInfo": "test"
}""")
        post_func.assert_called_once()

    def test_file_workspace_with_password(self):
        post_func = mock.MagicMock()
        wsp = PrepareWorkspacePublish(post_func)
        wsp.use_file_workspace_with_password()
        self.assertTrue(hasattr(wsp.workspace, 'set_path'))
        self.assertTrue(hasattr(wsp.workspace, 'set_password'))
        wsp.workspace.set_path('test')
        wsp.workspace.set_password('password')
        wsp.disallow_edit()
        wsp.avaliable_service_types.RESTMAP.select()
        wsp.execute()
        self.assertEqual(str(wsp), """{
  "isDataEditable": false,
  "servicesTypes": [
    "RESTMAP"
  ],
  "workspaceConnectionInfo": "server=test;password=password"
}""")
        post_func.assert_called_once()

    def test_oracle_workspace(self):
        post_func = mock.MagicMock()
        wsp = PrepareWorkspacePublish(post_func)
        wsp.use_oracle_workspace()
        self.assertTrue(hasattr(wsp.workspace, 'set_server_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_workspace_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_database_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_username'))
        self.assertTrue(hasattr(wsp.workspace, 'set_password'))
        wsp.workspace.set_server_name('servername')
        wsp.workspace.set_workspace_name('workspacename')
        wsp.workspace.set_database_name('databasename')
        wsp.workspace.set_username('username')
        wsp.workspace.set_password('password')
        wsp.disallow_edit()
        wsp.avaliable_service_types.RESTMAP.select()
        wsp.execute()
        self.assertEqual(str(wsp), """{
  "isDataEditable": false,
  "servicesTypes": [
    "RESTMAP"
  ],
  "workspaceConnectionInfo": "type=ORACLE;server=servername;name=workspacename;database=databasename;username=username;password=password"
}""")
        post_func.assert_called_once()

    def test_sql_workspace(self):
        post_func = mock.MagicMock()
        wsp = PrepareWorkspacePublish(post_func)
        wsp.use_sql_workspace()
        self.assertTrue(hasattr(wsp.workspace, 'set_server_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_workspace_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_database_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_username'))
        self.assertTrue(hasattr(wsp.workspace, 'set_password'))
        self.assertTrue(hasattr(wsp.workspace, 'set_driver'))
        wsp.workspace.set_server_name('servername')
        wsp.workspace.set_workspace_name('workspacename')
        wsp.workspace.set_database_name('databasename')
        wsp.workspace.set_username('username')
        wsp.workspace.set_password('password')
        wsp.workspace.set_driver('SQL Server')
        wsp.disallow_edit()
        wsp.avaliable_service_types.RESTMAP.select()
        wsp.execute()
        self.assertEqual(str(wsp), """{
  "isDataEditable": false,
  "servicesTypes": [
    "RESTMAP"
  ],
  "workspaceConnectionInfo": "type=SQL;server=servername;name=workspacename;database=databasename;username=username;password=password;driver=SQL Server"
}""")
        post_func.assert_called_once()

    def test_pgsql_workspace(self):
        post_func = mock.MagicMock()
        wsp = PrepareWorkspacePublish(post_func)
        wsp.use_pgsql_workspace()
        self.assertTrue(hasattr(wsp.workspace, 'set_server_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_workspace_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_database_name'))
        self.assertTrue(hasattr(wsp.workspace, 'set_username'))
        self.assertTrue(hasattr(wsp.workspace, 'set_password'))
        self.assertTrue(hasattr(wsp.workspace, 'set_driver'))
        wsp.workspace.set_server_name('servername')
        wsp.workspace.set_workspace_name('workspacename')
        wsp.workspace.set_database_name('databasename')
        wsp.workspace.set_username('username')
        wsp.workspace.set_password('password')
        wsp.workspace.set_driver('pgSQL Server')
        wsp.disallow_edit()
        wsp.avaliable_service_types.RESTMAP.select()
        wsp.execute()
        self.assertEqual(str(wsp), """{
  "isDataEditable": false,
  "servicesTypes": [
    "RESTMAP"
  ],
  "workspaceConnectionInfo": "type=PGSQL;server=servername;name=workspacename;database=databasename;username=username;password=password;driver=pgSQL Server"
}""")
        post_func.assert_called_once()
