import io
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.services.file_conversion import FileConversionService, OutputFormat, CONTENT_TYPE_MAP
from app.core.exceptions import FileConversionError

# Sample SVG content for testing
SAMPLE_SVG = """<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'>
    <style>
        :root {
            --test-color: #FF0000;
        }
        .test {
            fill: var(--test-color);
        }
    </style>
    <rect class='test' x='10' y='10' width='80' height='80' />
</svg>
"""

class TestFileConversionService:
    """Test suite for FileConversionService."""
    
    @pytest.fixture
    def service(self):
        """Create a FileConversionService instance for testing."""
        return FileConversionService()
    
    @pytest.fixture
    def sample_svg_file(self, tmp_path):
        """Create a sample SVG file for testing."""
        file_path = tmp_path / "test.svg"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_SVG)
        return file_path
    
    @patch("app.services.file_conversion.preprocess_svg_for_conversion")
    @patch("cairosvg.svg2png")
    def test_convert_svg_to_png(self, mock_svg2png, mock_preprocess, service):
        """Test converting SVG to PNG."""
        # Setup mocks
        mock_preprocess.return_value = SAMPLE_SVG
        mock_svg2png.return_value = b"mock_png_data"
        
        # Call the method
        result, content_type = service.convert_svg_to_format(SAMPLE_SVG, "png")
        
        # Verify results
        assert result == b"mock_png_data"
        assert content_type == "image/png"
        mock_preprocess.assert_called_once_with(SAMPLE_SVG)
        mock_svg2png.assert_called_once()
    
    @patch("app.services.file_conversion.preprocess_svg_for_conversion")
    @patch("cairosvg.svg2pdf")
    def test_convert_svg_to_pdf(self, mock_svg2pdf, mock_preprocess, service):
        """Test converting SVG to PDF."""
        # Setup mocks
        mock_preprocess.return_value = SAMPLE_SVG
        mock_svg2pdf.return_value = b"mock_pdf_data"
        
        # Call the method
        result, content_type = service.convert_svg_to_format(SAMPLE_SVG, "pdf")
        
        # Verify results
        assert result == b"mock_pdf_data"
        assert content_type == "application/pdf"
        mock_preprocess.assert_called_once_with(SAMPLE_SVG)
        mock_svg2pdf.assert_called_once()
    
    @patch("app.services.file_conversion.preprocess_svg_for_conversion")
    @patch("cairosvg.svg2png")
    @patch("PIL.Image.open")
    def test_convert_svg_to_jpg(self, mock_pil_open, mock_svg2png, mock_preprocess, service):
        """Test converting SVG to JPEG."""
        # Setup mocks
        mock_preprocess.return_value = SAMPLE_SVG
        mock_svg2png.return_value = b"mock_png_data"
        
        # Mock PIL Image handling
        mock_img = MagicMock()
        mock_img.convert.return_value = mock_img
        mock_pil_open.return_value.__enter__.return_value = mock_img
        
        # Mock BytesIO for JPEG output
        mock_buffer = MagicMock(spec=io.BytesIO)
        mock_buffer.getvalue.return_value = b"mock_jpg_data"
        
        with patch("io.BytesIO", return_value=mock_buffer):
            # Call the method
            result, content_type = service.convert_svg_to_format(SAMPLE_SVG, "jpg")
        
        # Verify results
        assert result == b"mock_jpg_data"
        assert content_type == "image/jpeg"
        mock_preprocess.assert_called_once_with(SAMPLE_SVG)
        mock_svg2png.assert_called_once()
        mock_img.convert.assert_called_once_with("RGB")
        mock_img.save.assert_called_once()
    
    def test_convert_svg_to_svg(self, service):
        """Test that SVG to SVG conversion simply preprocesses the SVG."""
        result, content_type = service.convert_svg_to_format(SAMPLE_SVG, "svg")
        
        # Since we're not mocking preprocess_svg_for_conversion here,
        # we expect the actual function to be called
        assert isinstance(result, bytes)
        assert content_type == "image/svg+xml"
    
    def test_unsupported_format(self, service):
        """Test that unsupported formats raise an error."""
        with pytest.raises(FileConversionError):
            service.convert_svg_to_format(SAMPLE_SVG, "gif")  # type: ignore
    
    @patch("builtins.open")
    @patch("app.services.file_conversion.FileConversionService.convert_svg_to_format")
    def test_convert_svg_file_to_format(self, mock_convert, mock_open, service, sample_svg_file):
        """Test converting an SVG file to a specific format."""
        # Setup mocks
        mock_convert.return_value = (b"mock_converted_data", "image/png")
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = SAMPLE_SVG
        mock_open.side_effect = [mock_file, MagicMock()]
        
        # Call the method
        output_path = Path("/tmp/output.png")
        result = service.convert_svg_file_to_format(sample_svg_file, "png", output_path)
        
        # Verify results
        assert result == output_path
        mock_convert.assert_called_once_with(SAMPLE_SVG, "png", 96)
        mock_open.assert_called_with(output_path, "wb")
    
    def test_convert_svg_file_not_found(self, service):
        """Test that FileNotFoundError is raised for non-existent files."""
        with pytest.raises(FileNotFoundError):
            service.convert_svg_file_to_format("/non/existent/file.svg", "png")
    
    def test_output_format_type(self):
        """Test that OutputFormat is a valid type annotation for format literals."""
        # This is more of a type checking test, but we can at least verify the values
        assert "svg" in OutputFormat.__args__  # type: ignore
        assert "png" in OutputFormat.__args__  # type: ignore
        assert "pdf" in OutputFormat.__args__  # type: ignore
        assert "jpg" in OutputFormat.__args__  # type: ignore
    
    def test_content_type_mapping(self):
        """Test that content type mapping is correct."""
        assert CONTENT_TYPE_MAP["svg"] == "image/svg+xml"
        assert CONTENT_TYPE_MAP["png"] == "image/png"
        assert CONTENT_TYPE_MAP["pdf"] == "application/pdf"
        assert CONTENT_TYPE_MAP["jpg"] == "image/jpeg"
        assert CONTENT_TYPE_MAP["jpeg"] == "image/jpeg" 