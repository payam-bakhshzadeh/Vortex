# gui/styles.py
class StyleSheet:
    """
    A class to hold the style sheets for the GUI components.
    """
    MAIN_WINDOW = """
    /* Main window background and font settings */
    background-color: #f0f0f0;
    font-family: Arial, sans-serif;
    """
    BUTTON = """
    /* Button background, text color, border, padding, and border-radius */
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    """
    STATUS_LABEL = """
    /* Status label text color and font size */
    color: #333;
    font-size: 14px;
    """
    DIALOG = """
    /* Dialog background and font settings */
    background-color: #ffffff;
    font-family: Arial, sans-serif;
    """
    DIALOG_LABEL = """
    /* Dialog label text color and font size */
    color: #333;
    font-size: 14px;
    """
    LABEL = """
    /* Label text color and font size */
    color: #333;
    font-size: 14px;
    """
    LINE_EDIT = """
    /* Line edit background, text color, border, padding, and border-radius */
    background-color: white;
    color: #333;
    border: 1px solid #ccc;
    padding: 5px;
    border-radius: 5px;
    """