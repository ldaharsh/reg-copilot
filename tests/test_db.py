import sqlite3
import pytest
from utils.db import initialize_db, save_chat, retrieve_recent_chats

@pytest.fixture
def setup_db():
    """Initialize a fresh test database before each test."""
    initialize_db()
    with sqlite3.connect("chat_history.db") as conn:
        conn.execute("DELETE FROM chat_history")  # ✅ Clears previous data before testing

def test_database_insert_and_retrieve(setup_db):
    """Test saving and retrieving chat interactions."""
    save_chat("Hello, AI!", "Hi there!")
    chats = retrieve_recent_chats(1)
    
    assert len(chats) == 1
    assert chats[0][0] == "Hello, AI!"
    assert chats[0][1] == "Hi there!"

def test_database_multiple_entries(setup_db):
    """Ensure multiple chat entries are stored correctly."""
    save_chat("How does CFR 113.300 apply?", "It defines potency tests.")
    save_chat("Summarize study X.", "Study X showed effectiveness.")

    chats = retrieve_recent_chats(2)
    
    assert len(chats) == 2
    assert "How does CFR 113.300 apply?" in [c[0] for c in chats]
    assert "Summarize study X." in [c[0] for c in chats]
