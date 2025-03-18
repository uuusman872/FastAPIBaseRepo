import unittest
from unittest.mock import AsyncMock, MagicMock
from service.users_service import UsersService
from models.models import User
from schema.users import UserCreateModel
from faker import Faker
import uuid
from datetime import datetime
import random
from sqlalchemy.future import select


class TestUserService(unittest.IsolatedAsyncioTestCase):
    async def test_create_user(self):
        mock_session = AsyncMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()

        user_data = UserCreateModel(
            username="testuser",
            firstname="test",
            lastname="user",
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

    async def test_get_user_by_email(self):
        mock_session = AsyncMock()
        fake = Faker()
        target_user = User(
            uid=uuid.uuid4(),
            email=fake.email(),
            role="user",
            username=fake.user_name(),
            password=fake.password(),
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            is_verified=fake.boolean(),
            created_at=fake.past_date(start_date="-1y"),
            updated_at=datetime.now(),
        )
        target_email = target_user.email
        mock_result = AsyncMock()
        mock_result.first.return_value = (target_user,)
        mock_session.execute.return_value = mock_result

        user_service = UsersService()
        returned_user = await user_service.get_user_by(email=target_email, session=mock_session)
        assert returned_user == target_user
        assert returned_user.email == target_email

    async def test_delete_user(self):
        mock_session = AsyncMock()

        # Create a mock user
        target_user = User(
            uid=uuid.uuid4(),
            email="test@example.com",
            role="user",
            username="testuser",
            password="hashedpassword",
            firstname="John",
            lastname="Doe",
            is_verified=True
        )

        target_email = target_user.email
        mock_result = AsyncMock()
        mock_result.first.return_value = (target_user,)
        mock_session.execute.return_value = mock_result
        mock_session.delete = AsyncMock()  
        mock_session.commit = AsyncMock()

        user_service = UsersService()
        delete_success = await user_service.delete_user(email=target_email, session=mock_session)
        assert delete_success is True
