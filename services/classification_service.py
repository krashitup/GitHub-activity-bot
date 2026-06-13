def classify_commit(message):
    """
    Analyzes a commit message and returns a standardized category.
    """
    # Convert the message to lowercase so we don't have to worry about capitalization
    message_lower = message.lower()
    
    # Check for common developer prefixes
    if message_lower.startswith('feat') or 'add ' in message_lower:
        return 'Feature'
    elif message_lower.startswith('fix') or 'bug' in message_lower:
        return 'Bug Fix'
    elif message_lower.startswith('docs') or 'readme' in message_lower:
        return 'Documentation'
    elif message_lower.startswith('refactor') or 'cleanup' in message_lower:
        return 'Refactor'
    else:
        return 'Other'

# Temporary test block
if __name__ == "__main__":
   
    test_messages = [
        "feat: added user authentication",
        "Fixing the broken login button",
        "Updated the README file",
        "Refactoring the database connection",
        "Initial commit"
    ]
    
    print("--- Testing Commit Classification ---")
    for msg in test_messages:
        category = classify_commit(msg)
        print(f"Message: '{msg}' -> Category: [{category}]")