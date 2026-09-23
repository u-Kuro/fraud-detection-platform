import pytest

from dags.shared.services.slack import create_blocks

class TestCreateBlocks:
    @staticmethod
    @pytest.fixture
    def default_blocks() -> list[dict]:
        return create_blocks(
            title="value",
            body="value"
        )

    @staticmethod
    @pytest.fixture
    def blocks_with_button() -> list[dict]:
        return create_blocks(
            title="value",
            body="value",
            buttons=[{}]
        )

    def test_return(self, default_blocks: list[dict]):
        assert isinstance(default_blocks, list)

    def test_buttons(
        self,
        default_blocks: list[dict],
        blocks_with_button: list[dict],
    ):
        assert len(default_blocks) == 2

        assert len(blocks_with_button) == 3
        assert blocks_with_button[2]["type"] == "actions"