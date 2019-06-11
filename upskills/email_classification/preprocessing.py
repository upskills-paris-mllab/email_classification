import re

# A collection of functions dedicated to preprocess and clean emails


# Improvement : drop the lowering of characters
def remove_subject_prefix(subject: str) -> str:
    """Remove "Re and fwd" from subject. Lower all subject characters.

    Args:
        subject: email subject

    Returns:
        subject without prefixes
    """
    return re.sub("((re)|(fwd?)).?: ", "", subject.lower())








