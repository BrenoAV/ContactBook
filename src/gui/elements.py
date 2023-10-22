"""
Elements of the Graphical Interface
"""
from typing import Any, Optional, Union
import PySimpleGUI as sg


# FONTS CONSTANTS
FONT_TITLE = ("Helvetica", 20)
FONT_DEFAULT = ("Helvetica", 12)


def sg_text_title(text: str):
    return sg.Text(
        text=text,
        expand_x=True,
        justification="center",
        font=FONT_TITLE,
    )


def sg_button_default(
    text: str,
    button_color: Optional[str] = None,
    key: Optional[str] = None,
    size: tuple[Optional[int], Optional[int]] = (None, None),
    pad: tuple[int, int] = (0, 0),
):
    return sg.Button(
        button_text=text,
        button_color=button_color,
        key=key,
        font=FONT_DEFAULT,
        size=size,
        use_ttk_buttons=True,
        pad=pad,
    )


def sg_text_default(text: str, justification: Optional[str] = None) -> sg.Text:
    return sg.Text(text=text, font=FONT_DEFAULT, justification=justification)


def sg_input_default(
    default_text: str = "", size: int = 30, key: Optional[str] = None
) -> sg.Input:
    return sg.Input(default_text=default_text, size=size, key=key, font=FONT_DEFAULT)


def sg_contact_table(
    values: list[list[Any]],
    headings: list[str],
    key: Optional[str] = None,
) -> Union[sg.Table, sg.Text]:
    if values:
        return sg.Table(
            values=values,
            headings=headings,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            key=key,
            expand_x=True,
            expand_y=True,
            font=FONT_DEFAULT,
            enable_events=True,
            enable_click_events=True,
            auto_size_columns=True,
        )
    return sg.Text(text="No data", font=FONT_DEFAULT)
