from griptape.tools import GoogleDriveClient
from unittest.mock import patch
from griptape.artifacts import ErrorArtifact
from google.auth.exceptions import MalformedError


class TestGoogleDriveClient:

    def test_list_files(self):
        value = {"folder_path": "root"}  # This can be any folder path you want to test
        result = GoogleDriveClient(owner_email="tony@griptape.ai", service_account_credentials={}).list_files(
            {"values": value}
        )
    
        assert isinstance(result, ErrorArtifact)
        assert "error retrieving files from Google Drive" in result.value

    def test_save_content_to_drive(self):
        value = {
            "path": "/path/to/your/file.txt",
            "content": "Sample content for the file."
        }
        result = GoogleDriveClient(
            owner_email="tony@griptape.ai",
            service_account_credentials={}
        ).save_content_to_drive({"values": value})

        assert isinstance(result, ErrorArtifact)
        assert "error saving file to Google Drive" in result.value

    @patch('griptape.tools.GoogleDriveClient._build_client')
    def test_download_files(self, mock_build_client):
        mock_build_client.side_effect = MalformedError('Mocked Error')
        value = {
            "file_paths": ["example_folder/example_file.txt"]
        }
        try:
            result = GoogleDriveClient(
                owner_email="tony@griptape.ai",
                service_account_credentials={}
            ).download_files({"values": value})
            assert False, "Expected MalformedError was not raised"
        except MalformedError as e:
            assert str(e) == 'Mocked Error'

    @patch('griptape.tools.GoogleDriveClient._build_client')
    def test_search_files(self, mock_build_client):  # <-- Updated method name
        mock_build_client.side_effect = MalformedError('Mocked Error')
        value = {
            "search_mode": "name",
            "file_name": "search_file_name.txt"
        }
        result = GoogleDriveClient(
            owner_email="tony@griptape.ai",
            service_account_credentials={}
        ).search_files({"values": value})  # <-- Updated method call

        assert isinstance(result, ErrorArtifact)
        assert "error searching for file due to malformed credentials" in result.value