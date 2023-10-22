"""
Module for window management

Author: BrenoAV
"""
from typing import Optional, Union

import PySimpleGUI as sg

from src.gui.elements import (
    sg_button_default,
    sg_contact_table,
    sg_input_default,
    sg_text_default,
    sg_text_title,
)

# TODO: Transform this into a database
VALUES: list[list[Union[int, str]]] = [
    [1, "Linda", "Technical Lead", "linda@example.com"],
    [2, "Joe", "Senior Web Developer", "joe@example"],
]

HEADINGS: list[str] = ["id", "name", "job", "email"]


class MainWindow:
    def __init__(self) -> None:
        title = "Contact Book - Python"
        layout = [
            [sg_text_title(text="Contact Book Interface")],
            [
                sg.Column(
                    [
                        [
                            sg_contact_table(
                                values=VALUES, headings=HEADINGS, key="-DATABASE-"
                            )
                        ]
                    ],
                    justification="c",
                    expand_x=True,
                    expand_y=True,
                ),
                sg.VerticalSeparator(),
                sg.Column(
                    [
                        [
                            sg_button_default(
                                text="Add...",
                                pad=(0, 10),
                                size=(10, 1),
                                key="-BUTTON ADD-",
                            )
                        ],
                        [
                            sg_button_default(
                                text="Edit",
                                pad=(0, 10),
                                size=(10, 1),
                                key="-BUTTON EDIT-",
                            )
                        ],
                        [
                            sg_button_default(
                                text="Delete",
                                pad=(0, 10),
                                size=(10, 1),
                                key="-BUTTON DEL-",
                            )
                        ],
                        [sg.HorizontalSeparator()],
                        [
                            sg_button_default(
                                text="Clear all",
                                button_color="red",
                                pad=(0, 20),
                                size=(10, 1),
                                key="-BUTTON CLEAR ALL-",
                            )
                        ],
                    ],
                    justification="c",
                    vertical_alignment="top",
                ),
            ],
        ]
        self.window = sg.Window(
            title=title, layout=layout, resizable=True, finalize=True
        )
        self.window.set_min_size((600, 480))

    def run(self) -> None:
        global VALUES
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED,):
                break
            if event == "-BUTTON ADD-":
                # Get the size of the table to be add if add new records
                table_size = len(self.window["-DATABASE-"].get())
                add_window = AddWindow()
                add_window.run(table_size=table_size)
                self.reset_index_values(VALUES)
                self.window["-DATABASE-"].update(values=VALUES)
            if event == "-BUTTON EDIT-":
                # Checking if the row is selected
                if values["-DATABASE-"]:
                    row_index: int = values["-DATABASE-"][0]
                    edit_window = EditWindow(VALUES[row_index])
                    new_values = edit_window.run()
                    if new_values:
                        VALUES[row_index] = new_values
                        self.reset_index_values(VALUES)
                        self.window["-DATABASE-"].update(values=VALUES)
            elif event == "-BUTTON DEL-":
                # Checking if the row is selected
                if values["-DATABASE-"]:
                    index = values["-DATABASE-"][0]
                    ch = sg.popup_yes_no(
                        f"Do you want delete the selected entry with the id: {VALUES[index][0]}?",
                        title="Delete Confirmation",
                    )
                    if ch.lower() == "yes":
                        VALUES.pop(index)
                        self.reset_index_values(VALUES)
                        self.window["-DATABASE-"].update(values=VALUES)
            elif event == "-BUTTON CLEAR ALL-":
                ch = sg.popup_yes_no(
                    "Do you want delete ALL the entries?",
                    title="Clear All Confirmation",
                )
                if ch.lower() == "yes":
                    VALUES = []
                    self.window["-DATABASE-"].update(values=VALUES)
        self.window.close()

    @staticmethod
    def reset_index_values(values):
        # Reset the index values
        if values:
            count = 1
            for i in range(len(values)):
                values[i][0] = count
                count += 1
            return values


class AddWindow:
    def __init__(self) -> None:
        col1 = [
            [sg_text_default("Name: ")],
            [sg_text_default("Job: ")],
            [sg_text_default("Email: ")],
        ]
        col2 = [
            [sg_input_default(key="-INPUT NAME-")],
            [sg_input_default(key="-INPUT JOB-")],
            [sg_input_default(key="-INPUT EMAIL-")],
        ]
        layout = [
            [
                [sg.Column(col1), sg.Column(col2)],
                [
                    sg_button_default(
                        "Cancel", button_color="red", key="-BUTTON CANCEL-", pad=(10, 0)
                    ),
                    sg_button_default(
                        "OK", button_color="green", key="-BUTTON OK-", pad=(10, 0)
                    ),
                ],
            ],
        ]
        self.window = sg.Window(
            title="Add Contact", layout=layout, element_justification="c", finalize=True
        )

    def run(self, table_size: int) -> None:
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, "-BUTTON CANCEL-"):
                break
            if event == "-BUTTON OK-":
                i = table_size + 1
                name = values["-INPUT NAME-"]
                job = values["-INPUT JOB-"]
                email = values["-INPUT EMAIL-"]
                VALUES.append([i, name, job, email])
                i += 1
                break

        self.window.close()


class EditWindow:
    def __init__(self, old_values) -> None:
        self.old_values = old_values
        col1 = [
            [sg_text_default("")],
            [sg_text_default("Id: ")],
            [sg_text_default("Name:")],
            [sg_text_default("Job:")],
            [sg_text_default("Email:")],
        ]
        col2 = [
            [sg_text_default("Old Value")],
            [sg_text_default(old_values[0])],
            [sg_text_default(old_values[1])],
            [sg_text_default(old_values[2])],
            [sg_text_default(old_values[3])],
        ]
        col3 = [
            [sg_text_default("New Value")],
            [sg_text_default(text=old_values[0])],
            [sg_input_default(default_text=old_values[1], key="-INPUT NEW NAME-")],
            [sg_input_default(default_text=old_values[2], key="-INPUT NEW JOB-")],
            [sg_input_default(default_text=old_values[3], key="-INPUT NEW EMAIL-")],
        ]
        layout = [
            [sg.Column(col1), sg.Column(col2), sg.Column(col3)],
            [
                sg_button_default(
                    text="Cancel",
                    button_color="red",
                    key="-BUTTON CANCEL-",
                    pad=(10, 0),
                ),
                sg_button_default(
                    text="Modify",
                    button_color="green",
                    key="-BUTTON MODIFY-",
                    pad=(10, 0),
                ),
            ],
        ]
        self.window = sg.Window(
            "Edit", layout=layout, finalize=True, element_justification="center"
        )

    def run(self) -> Optional[list[Union[int, str]]]:
        while True:
            event, _ = self.window.read()
            if event in (sg.WIN_CLOSED, "-BUTTON CANCEL-"):
                break
            if event == "-BUTTON MODIFY-":
                new_values = [
                    self.old_values[0],
                    self.window["-INPUT NEW NAME-"].get(),
                    self.window["-INPUT NEW JOB-"].get(),
                    self.window["-INPUT NEW EMAIL-"].get(),
                ]
                self.window.close()
                return new_values
        self.window.close()
        return None
