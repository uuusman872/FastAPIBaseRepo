import unittest
from unittest.mock import AsyncMock, MagicMock
import asyncio
from service.users_service import UsersService
from models import User
from schema.users import UserCreateModel

class TestUserService(unittest.IsolatedAsyncioTestCase):
    async def test_create_user(self):
        mock_session = AsyncMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()

        user_data = UserCreateModel(
            username="testuser",
            email="test@example.com",
            password="securepassword"
        )

        user_service = UsersService()

        user = await user_service.create_user(user_data, mock_session)

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertNotEqual(user.password, "securepassword")

        mock_session.add.assert_called_once_with(user)
        
        mock_session.commit.assert_awaited_once()

# if __name__ == "__main__":
#     unittest.main()
