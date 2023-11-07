import pytest
from unittest.mock import patch, MagicMock
from _connections import conn_id_to_name, dbs_to_update, files_conns, files_conn_ids, files_folders


CONN_TYPE = 'sftp'
FILE_CONN_IDS = ['file_sftp_1', 'file_sftp_2']


@pytest.fixture
def mock_session():
    with patch('airflow.settings.Session') as session:
        yield session


@pytest.fixture
def mock_connection():
    with patch('airflow.models.Connection') as conn:
        yield conn


def test_conn_id_to_name():
    assert conn_id_to_name('db_dev') == 'dev'
    assert conn_id_to_name('db_prod') == 'prod'


def test_dbs_to_update(mock_session):
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = [
        MagicMock(conn_id='db_dev'),
        MagicMock(conn_id='db_prod'),
    ]
    assert dbs_to_update() == ['db_dev', 'db_prod']


def test_files_conns(mock_session, mock_connection):
    conn_type = 'ftp'
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = [
        mock_connection(conn_id='file_ftp_1', conn_type=conn_type),
        mock_connection(conn_id='file_ftp_2', conn_type=conn_type),
    ]
    assert len(list(files_conns(conn_type))) == 2


def test_files_conn_ids(mock_session, mock_connection):
    mock_conn_1 = MagicMock()
    mock_conn_1.conn_id = FILE_CONN_IDS[0]
    mock_conn_2 = MagicMock()
    mock_conn_2.conn_id = FILE_CONN_IDS[1]
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = [
        mock_conn_1,
        mock_conn_2,
    ]
    conn_ids = files_conn_ids(CONN_TYPE)
    assert conn_ids == FILE_CONN_IDS, "The conn_ids did not match expected values"


def test_files_folders(mock_session, mock_connection):
    conn_type = 'gcs'
    mock_connection_instance = MagicMock()
    mock_connection_instance.conn_id = 'file_gcs_1'
    mock_connection_instance.extra_dejson.get.return_value = '/path/to/gcs'

    mock_session.return_value.query.return_value.filter.return_value.all.return_value = [
        mock_connection_instance
    ]

    assert files_folders(conn_type) == ['/path/to/gcs']
