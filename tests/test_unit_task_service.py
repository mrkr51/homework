import pytest
from unittest.mock import AsyncMock
from app.services.tasks import TaskService
from app.schemas import TaskCreate


@pytest.mark.asyncio
async def test_create_task_service_mock():
    mock_repo = AsyncMock()
    mock_repo.create_task.return_value = AsyncMock(
        id=1, title="Unit Task", description="Desc", is_done=False, owner_id=1
    )

    service = TaskService(db=AsyncMock())
    service.repo = mock_repo

    task_data = TaskCreate(title="Unit Task", description="Desc")
    result = await service.create_new_task(task_data, user_id=1)

    assert result.title == "Unit Task"
    mock_repo.create_task.assert_called_once()