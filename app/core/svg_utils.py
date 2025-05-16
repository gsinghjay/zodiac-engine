import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def parse_css_variables(svg_content: str) -> Dict[str, str]:
    """
    Parses CSS variables defined in a :root block within SVG styles.
    
    Args:
        svg_content (str): SVG content as a string
        
    Returns:
        Dict[str, str]: Dictionary of variable names (--var-name) and their values
    """
    variables: Dict[str, str] = {}
    
    # Find style tags
    style_tags = re.findall(r'<style.*?>(.*?)</style>', svg_content, re.DOTALL | re.IGNORECASE)
    var_pattern = re.compile(r'(--[\w-]+)\s*:\s*([^;]+);')
    
    for style_content in style_tags:
        # Look for :root block
        root_match = re.search(r':root\s*\{(.*?)\}', style_content, re.DOTALL | re.IGNORECASE)
        if root_match:
            root_content = root_match.group(1)
            for match in var_pattern.finditer(root_content):
                var_name = match.group(1).strip()
                var_value = match.group(2).strip()
                variables[var_name] = var_value
                logger.debug(f"Found CSS variable: {var_name} = {var_value}")
    
    if not variables:
        logger.warning("No CSS variables found in the SVG content")
    else:
        logger.info(f"Found {len(variables)} CSS variables in the SVG content")
    
    return variables

def resolve_nested_variables(value: str, variables: Dict[str, str], visited: set = None) -> str:
    """
    Recursively resolves nested variable references.
    
    Args:
        value (str): The value potentially containing variable references
        variables (Dict[str, str]): Dictionary of variable names and their values
        visited (set): Set of already visited variables to prevent infinite recursion
        
    Returns:
        str: The value with all nested variables resolved
    """
    if visited is None:
        visited = set()
    
    # Check if this is a variable reference
    var_ref_match = re.match(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)', value)
    if var_ref_match:
        var_name = var_ref_match.group(1)
        default_value = var_ref_match.group(2) if var_ref_match.group(2) else 'inherit'
        
        # Prevent infinite recursion
        if var_name in visited:
            logger.warning(f"Circular reference detected for variable {var_name}")
            return default_value
        
        visited.add(var_name)
        
        if var_name in variables:
            # Recursively resolve nested variables in the variable's value
            resolved_value = resolve_nested_variables(variables[var_name], variables, visited)
            return resolved_value
        else:
            logger.warning(f"Variable {var_name} not found, using default value: {default_value}")
            return default_value
    
    # Check for nested variable references within the value
    var_usage_pattern = re.compile(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)')
    
    def replacer(match):
        var_name = match.group(1)
        default_value = match.group(2) if match.group(2) else 'inherit'
        
        # Prevent infinite recursion
        if var_name in visited:
            logger.warning(f"Circular reference detected for variable {var_name}")
            return default_value
        
        new_visited = visited.copy()
        new_visited.add(var_name)
        
        if var_name in variables:
            # Recursively resolve nested variables
            resolved_value = resolve_nested_variables(variables[var_name], variables, new_visited)
            return resolved_value
        else:
            logger.warning(f"Variable {var_name} not found, using default value: {default_value}")
            return default_value
    
    # Replace all var() references in the value
    return var_usage_pattern.sub(replacer, value)

def substitute_css_variables(svg_content: str, variables: Dict[str, str]) -> str:
    """
    Substitutes var(--name) calls in style attributes with actual values.
    Handles nested CSS variable references by recursively resolving them.
    
    Args:
        svg_content (str): SVG content as a string
        variables (Dict[str, str]): Dictionary of variable names and their values
        
    Returns:
        str: SVG content with variables substituted
    """
    if not variables:
        logger.warning("No variables provided for substitution")
        # Continue processing to handle defaults in var() calls
    
    # Resolve nested variable references in the variable definitions
    resolved_variables = {}
    for name, value in variables.items():
        if 'var(--' in value:
            resolved_variables[name] = resolve_nested_variables(value, variables)
        else:
            resolved_variables[name] = value
    
    # Use the resolved variables
    variables = resolved_variables
    
    var_usage_pattern = re.compile(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)')
    
    def replacer(match):
        var_name = match.group(1)
        default_value = match.group(2) if match.group(2) else 'inherit'
        
        if var_name in variables:
            replacement = variables[var_name]
            logger.debug(f"Replacing {var_name} with {replacement}")
            return replacement
        else:
            logger.warning(f"Variable {var_name} not found, using default: {default_value}")
            return default_value
    
    # Multiple passes to handle nested variables
    max_passes = 5  # Limit the number of passes to avoid infinite loops
    current_svg = svg_content
    
    for i in range(max_passes):
        # Use regex to replace var() in style attributes
        new_svg = var_usage_pattern.sub(replacer, current_svg)
        
        # If no more replacements were made, we're done
        if new_svg == current_svg:
            logger.info(f"Variable substitution completed after {i+1} passes")
            break
        
        current_svg = new_svg
    
    # Count the number of substitutions
    original_count = len(re.findall(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)', svg_content))
    remaining_count = len(re.findall(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)', current_svg))
    
    if original_count > 0:
        logger.info(f"Substituted {original_count - remaining_count} of {original_count} CSS variable usages")
    
    if remaining_count > 0:
        logger.warning(f"{remaining_count} CSS variable usages could not be substituted")
    
    return current_svg

def preprocess_svg_for_conversion(svg_content: str) -> str:
    """
    Preprocesses SVG content for conversion by parsing CSS variables and substituting them.
    
    Args:
        svg_content (str): SVG content as a string
        
    Returns:
        str: Preprocessed SVG content ready for conversion
    """
    # Parse CSS variables
    variables = parse_css_variables(svg_content)
    
    # Substitute variables
    processed_svg = substitute_css_variables(svg_content, variables)
    
    return processed_svg