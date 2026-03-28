"""
Utility functions for the application
"""


def print_welcome():
    """
    Displays a decorative welcome message in the console.
    This is used when the CLI application starts to provide visual context.
    """
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        🛍️  WEAVIATE E-COMMERCE ASSISTANT - AGENTS DEMO        ║
║                                                                ║
║   An intelligent AI-powered shopping assistant powered by      ║
║   Weaviate Query Agent, Personalization, and Transformation    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)


def print_menu():
    """
    Displays the main menu of the CLI application with available options.
    Each option corresponds to a specific demo or mode.
    """
    print("""
┌─────────────────────────────────────────────────────────────┐
│                    MAIN MENU                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. Run Demo Queries (5 different query types)               │
│ 2. Personalization Agent Demo                              │
│ 3. Transformation Agent Demo                               │
│ 4. Interactive Mode (Ask questions yourself)               │
│ 5. Run All Demos                                           │
└─────────────────────────────────────────────────────────────┘
    """)


def format_response(response: dict) -> str:
    """
    Formats the raw response dictionary from an agent into a human-readable string.
    
    Args:
        response (dict): The dictionary containing 'success' and 'answer' keys.
        
    Returns:
        str: A formatted string for display to the user.
    """
    if response.get('success'):
        return response.get('answer', 'No answer provided')
    else:
        return f"Error: {response.get('answer', 'Unknown error')}"

