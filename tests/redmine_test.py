from lisum_chat.app import redmine
import dotenv

dotenv.load_dotenv()


def test_redmine_auth():
    redmine.auth()


def test_redmine_get_projects():
    search_results = redmine.search("project")
    assert search_results
