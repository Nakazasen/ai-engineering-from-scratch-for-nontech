import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('ai-learning-companion'))
from unittest.mock import patch
from ai_tutor_proxy.retrieval import retrieve_top_chunks

class TestRetrieval(unittest.TestCase):
    
    @patch('os.path.exists')
    @patch('builtins.open')
    def test_retrieve_chunks_dict_format(self, mock_file_open, mock_exists):
        # 1. Mock/load fixture dạng dict có "chunks"
        mock_exists.return_value = True
        mock_data = '{"schema_version": 1, "chunk_count": 1, "chunks": [{"chunk_id": "c1", "lesson_id": "L1", "title": "RAG", "heading": "RAG concept", "text": "RAG là gì?", "source_path": "path/to/doc", "source_type": "lesson"}]}'
        mock_file_open.return_value.__enter__.return_value.read.return_value = mock_data
        
        # Gọi retrieve_top_chunks
        chunks = retrieve_top_chunks("RAG là gì?")
        
        # Assert không crash và trả list
        self.assertIsInstance(chunks, list)
        self.assertEqual(len(chunks), 1)
        
        # Assert item có lesson_id/text/source_doc_path
        chunk = chunks[0]
        self.assertEqual(chunk["lesson_id"], "L1")
        self.assertEqual(chunk["text"], "RAG là gì?")
        self.assertEqual(chunk["source_doc_path"], "path/to/doc")
        self.assertEqual(chunk["title"], "RAG")
        self.assertEqual(chunk["heading"], "RAG concept")
        self.assertEqual(chunk["chunk_id"], "c1")
        self.assertEqual(chunk["source_type"], "lesson")
        self.assertEqual(chunk["score"], 1.0)

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_retrieve_chunks_list_format(self, mock_file_open, mock_exists):
        # 2. Mock/load dạng list chunks trực tiếp
        mock_exists.return_value = True
        mock_data = '[{"chunk_id": "c2", "lesson_id": "L2", "title": "Embedding", "heading": "Concept", "text": "embedding là gì?", "source_doc_path": "path/to/doc2", "source_type": "lesson"}]'
        mock_file_open.return_value.__enter__.return_value.read.return_value = mock_data
        
        chunks = retrieve_top_chunks("embedding là gì?")
        self.assertIsInstance(chunks, list)
        self.assertEqual(len(chunks), 1)
        chunk = chunks[0]
        self.assertEqual(chunk["lesson_id"], "L2")
        self.assertEqual(chunk["source_doc_path"], "path/to/doc2")

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_retrieve_chunks_invalid_format(self, mock_file_open, mock_exists):
        # 3. Test invalid format: index là dict không có "chunks"
        mock_exists.return_value = True
        mock_data = '{"schema_version": 1, "chunk_count": 0}'
        mock_file_open.return_value.__enter__.return_value.read.return_value = mock_data
        
        chunks = retrieve_top_chunks("RAG là gì?")
        self.assertEqual(chunks, [])

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_retrieve_chunks_non_list_chunks(self, mock_file_open, mock_exists):
        # 4. Test chunks không phải list
        mock_exists.return_value = True
        mock_data = '{"schema_version": 1, "chunks": "not_a_list"}'
        mock_file_open.return_value.__enter__.return_value.read.return_value = mock_data
        
        chunks = retrieve_top_chunks("RAG là gì?")
        self.assertEqual(chunks, [])

    @patch('os.path.exists')
    @patch('builtins.open')
    def test_retrieve_chunks_with_non_dict_items(self, mock_file_open, mock_exists):
        # 5. Test dict index có list chunks chứa item không phải dict (non-dict item)
        mock_exists.return_value = True
        mock_data = '{"chunks": ["string_item_here", {"chunk_id": "c1", "lesson_id": "L1", "title": "RAG", "text": "RAG là gì?"}]}'
        mock_file_open.return_value.__enter__.return_value.read.return_value = mock_data
        
        chunks = retrieve_top_chunks("RAG")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["chunk_id"], "c1")

if __name__ == "__main__":
    unittest.main()
