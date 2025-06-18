import pytest
from utils.file_loader import read_file, chunk_text
from pathlib import Path

@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file."""
    file = tmp_path / "sample.txt"
    file.write_text("This is a test document.\nIt contains multiple lines.")
    return file

def test_file_loading_text(sample_text_file):
    """Test reading a simple text file."""
    content = read_file(str(sample_text_file))
    assert "This is a test document." in content
    assert "It contains multiple lines." in content

def test_chunking_text():
    """Test token-based chunking."""
    sample_text = "This is a long text. " * 300
    chunks = list(chunk_text(sample_text, max_tokens=100))
    
    assert len(chunks) > 1
    assert all(len(chunk) > 50 for chunk in chunks)  # Ensure proper splitting
