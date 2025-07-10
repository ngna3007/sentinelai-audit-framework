"""
Mock pyjq module for Python 3.13 compatibility.
This provides basic JSON path functionality to replace pyjq.
"""
import json


def all(path, data):
    """
    Simple implementation of pyjq.all() for basic JSON path queries.
    
    Args:
        path: JSON path string (e.g., '.Reservations[].Instances[]')
        data: JSON data to query
    
    Returns:
        List of matching elements
    """
    if not path.startswith('.'):
        return data.get(path, []) if isinstance(data, dict) else []
    
    # Remove leading dot
    path = path[1:]
    
    # Simple path parsing for common patterns
    if not path:
        return [data]
    
    parts = path.split('.')
    current = data
    
    for part in parts:
        if '[]' in part:
            # Handle array notation
            key = part.replace('[]', '')
            if key:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return []
            
            # Flatten if it's a list of lists
            if isinstance(current, list):
                flattened = []
                for item in current:
                    if isinstance(item, list):
                        flattened.extend(item)
                    else:
                        flattened.append(item)
                current = flattened
        else:
            # Regular key access
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list):
                # Apply to each item in the list
                new_current = []
                for item in current:
                    if isinstance(item, dict) and part in item:
                        new_current.append(item[part])
                current = new_current
            else:
                return []
    
    return current if isinstance(current, list) else [current]


def first(path, data):
    """
    Get the first matching element.
    
    Args:
        path: JSON path string
        data: JSON data to query
    
    Returns:
        First matching element or None
    """
    results = all(path, data)
    return results[0] if results else None 