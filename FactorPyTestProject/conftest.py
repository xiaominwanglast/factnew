import pytest
from utils.MongoUtil import MongoPyUtilPort
#命令行传入执行参数
def pytest_addoption(parser):
    parser.addoption(
        "--envopt", action="store", default="T1", help="my option: T1 or T2 or T3"
    )

@pytest.fixture
def envopt(request):
    return request.config.getoption("--envopt")