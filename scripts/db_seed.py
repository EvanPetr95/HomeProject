#!/usr/bin/env python3
"""
Database seeding script for development/testing purposes.
Creates a user, foundation, grants, and grant feedback.
"""

import asyncio
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import DATABASE_URL
from app.database import Base
from app.foundation.models import Foundation
from app.grant.models import Grant
from app.grant_feedback.enums import ReactionEnum
from app.grant_feedback.models import GrantFeedback
from app.user.models import User
from lib.utils import PWD_CONTEXT

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def seed_database():
    """Seed the database with test data."""
    print("Starting database seeding...")

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created")

    async with async_session_maker() as session:
        try:
            # Check if user already exists
            result = await session.execute(
                select(User).where(User.email == "demo@example.com")
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print("Demo user already exists. Skipping seed...")
                return

            # Create a demo user
            user = User(
                id=UUID("00000000-0000-0000-0000-000000000001"),
                name="Demo User",
                email="demo@example.com",
                password=PWD_CONTEXT.hash("demo123"),
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
            session.add(user)
            print(f"Created user: {user.email}")

            # Create a foundation
            foundation = Foundation(
                id=UUID("00000000-0000-0000-0000-000000000002"),
                name="Tech Innovation Foundation",
                logo_url="https://example.com/logos/tech-innovation.png",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
            session.add(foundation)
            print(f"Created foundation: {foundation.name}")

            # Create multiple grants
            grants_data = [
                {
                    "id": UUID("00000000-0000-0000-0000-000000000010"),
                    "name": "AI Research Grant 2024",
                    "amount": 50000,
                    "deadline": datetime.now(UTC) + timedelta(days=60),
                    "location": "San Francisco, CA",
                    "area": "Artificial Intelligence",
                },
                {
                    "id": UUID("00000000-0000-0000-0000-000000000011"),
                    "name": "Green Tech Innovation Fund",
                    "amount": 75000,
                    "deadline": datetime.now(UTC) + timedelta(days=90),
                    "location": "Seattle, WA",
                    "area": "Environmental Technology",
                },
                {
                    "id": UUID("00000000-0000-0000-0000-000000000012"),
                    "name": "EdTech Development Grant",
                    "amount": 30000,
                    "deadline": datetime.now(UTC) + timedelta(days=45),
                    "location": "Austin, TX",
                    "area": "Education Technology",
                },
                {
                    "id": UUID("00000000-0000-0000-0000-000000000013"),
                    "name": "Healthcare Innovation Award",
                    "amount": 100000,
                    "deadline": datetime.now(UTC) + timedelta(days=120),
                    "location": "Boston, MA",
                    "area": "Healthcare",
                },
                {
                    "id": UUID("00000000-0000-0000-0000-000000000014"),
                    "name": "Blockchain Research Initiative",
                    "amount": 60000,
                    "deadline": datetime.now(UTC) + timedelta(days=75),
                    "location": "New York, NY",
                    "area": "Blockchain & Cryptocurrency",
                },
            ]

            grants = []
            for grant_data in grants_data:
                grant = Grant(
                    id=grant_data["id"],
                    foundation_id=foundation.id,
                    name=grant_data["name"],
                    amount=grant_data["amount"],
                    deadline=grant_data["deadline"],
                    location=grant_data["location"],
                    area=grant_data["area"],
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                )
                session.add(grant)
                grants.append(grant)
                print(f"Created grant: {grant.name} (${grant.amount:,})")

            # Create grant feedback for some grants
            feedbacks_data = [
                {
                    "grant_index": 0,  # AI Research Grant
                    "reaction": ReactionEnum.LIKE,
                    "comment": "This looks like a perfect fit for our AI research project!",
                },
                {
                    "grant_index": 1,  # Green Tech Innovation Fund
                    "reaction": ReactionEnum.LIKE,
                    "comment": "Great opportunity for sustainable tech development.",
                },
                {
                    "grant_index": 2,  # EdTech Development Grant
                    "reaction": ReactionEnum.DISLIKE,
                    "comment": "The amount seems too low for our project scope.",
                },
                {
                    "grant_index": 3,  # Healthcare Innovation Award
                    "reaction": ReactionEnum.LIKE,
                    "comment": "Excellent funding amount and timeline. Will definitely apply!",
                },
            ]

            for feedback_data in feedbacks_data:
                grant = grants[feedback_data["grant_index"]]
                feedback = GrantFeedback(
                    grant_id=grant.id,
                    user_id=user.id,
                    reaction=feedback_data["reaction"],
                    comment=feedback_data["comment"],
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                )
                session.add(feedback)
                print(f"Created feedback: {feedback.reaction.name} for '{grant.name}'")

            # Commit all changes
            await session.commit()
            print("\n<� Database seeding completed successfully!")
            print("\n=� Summary:")
            print("   - Created 1 user (email: demo@example.com, password: demo123)")
            print("   - Created 1 foundation")
            print(f"   - Created {len(grants)} grants")
            print(f"   - Created {len(feedbacks_data)} grant feedbacks")
            print("\n=� Use these credentials to login:")
            print("   Email: demo@example.com")
            print("   Password: demo123")

        except Exception as e:
            await session.rollback()
            print(f"\nL Error during seeding: {e}")
            raise


async def clear_database():
    """Clear all data from the database."""
    print("Clearing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Database cleared")


async def main():
    """Main entry point for the seeding script."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        await clear_database()
    else:
        await seed_database()

    # Close engine
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
