import pytest
from app.core.svg_utils import parse_css_variables, substitute_css_variables, preprocess_svg_for_conversion

SAMPLE_SVG_WITH_VARS = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
    <style>
        :root {
            --chart-bg-color: #ffffff;
            --chart-line-color: #000000;
            --planet-fill-color: #ff0000;
            --text-color: #333333;
        }
        
        .chart-background {
            fill: var(--chart-bg-color);
        }
        
        .chart-line {
            stroke: var(--chart-line-color);
            stroke-width: 1px;
        }
        
        .planet-circle {
            fill: var(--planet-fill-color);
        }
        
        .chart-text {
            fill: var(--text-color);
            font-family: Arial, sans-serif;
        }
    </style>
    <rect class="chart-background" x="0" y="0" width="500" height="500" />
    <circle class="planet-circle" cx="250" cy="250" r="20" />
    <line class="chart-line" x1="0" y1="250" x2="500" y2="250" />
    <text class="chart-text" x="250" y="300">Test Chart</text>
</svg>"""


def test_parse_css_variables():
    """Test parsing CSS variables from SVG content."""
    variables = parse_css_variables(SAMPLE_SVG_WITH_VARS)
    
    assert len(variables) == 4
    assert variables["--chart-bg-color"] == "#ffffff"
    assert variables["--chart-line-color"] == "#000000"
    assert variables["--planet-fill-color"] == "#ff0000"
    assert variables["--text-color"] == "#333333"


def test_substitute_css_variables():
    """Test substituting CSS variables in SVG content."""
    variables = {
        "--chart-bg-color": "#ffffff",
        "--chart-line-color": "#000000",
        "--planet-fill-color": "#ff0000",
        "--text-color": "#333333"
    }
    
    result = substitute_css_variables(SAMPLE_SVG_WITH_VARS, variables)
    
    # Check that variables have been replaced
    assert 'fill: #ffffff' in result
    assert 'stroke: #000000' in result
    assert 'fill: #ff0000' in result
    assert 'fill: #333333' in result
    
    # Ensure no var() calls remain
    assert 'var(--chart-bg-color)' not in result
    assert 'var(--chart-line-color)' not in result
    assert 'var(--planet-fill-color)' not in result
    assert 'var(--text-color)' not in result


def test_preprocess_svg_for_conversion():
    """Test the complete preprocessing function."""
    result = preprocess_svg_for_conversion(SAMPLE_SVG_WITH_VARS)
    
    # Check that variables have been replaced
    assert 'fill: #ffffff' in result
    assert 'stroke: #000000' in result
    assert 'fill: #ff0000' in result
    assert 'fill: #333333' in result
    
    # Ensure no var() calls remain
    assert 'var(--chart-bg-color)' not in result
    assert 'var(--chart-line-color)' not in result
    assert 'var(--planet-fill-color)' not in result
    assert 'var(--text-color)' not in result


def test_parse_css_variables_empty():
    """Test parsing CSS variables from SVG content without variables."""
    svg_without_vars = """<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
        <rect x="0" y="0" width="500" height="500" fill="#ffffff" />
    </svg>"""
    
    variables = parse_css_variables(svg_without_vars)
    assert len(variables) == 0


def test_substitute_css_variables_with_defaults():
    """Test substituting CSS variables with defaults."""
    svg_with_defaults = """<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
        <style>
            .chart-background {
                fill: var(--chart-bg-color, #eeeeee);
            }
        </style>
        <rect class="chart-background" x="0" y="0" width="500" height="500" />
    </svg>"""
    
    # Empty variables dictionary, should use defaults
    variables = {}
    
    result = substitute_css_variables(svg_with_defaults, variables)
    assert 'fill: #eeeeee' in result 