import enum


class ContentType(str, enum.Enum):
    """
    Enumeration of content types.
    """
    VIDEO = "video"
    AUDIO = "audio"
