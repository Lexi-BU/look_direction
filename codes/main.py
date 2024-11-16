import pandas as pd
from tkinter import (
    Tk,
    Label,
    Entry,
    Button,
    StringVar,
    OptionMenu,
    Checkbutton,
    IntVar,
    messagebox,
    ttk,
    DISABLED,
    NORMAL,
    Scrollbar,
    VERTICAL,
    HORIZONTAL,
)
import datetime
import numpy as np

# Load the CSV file (replace 'your_file.csv' with the actual file path)
data = pd.read_csv("../data/20241114_LEXIAngleData_20250302Landing.csv")
data["epoch_utc"] = pd.to_datetime(data["epoch_utc"])
# Set the timezones to UTC
data["epoch_utc"] = data["epoch_utc"].dt.tz_localize("UTC")


# Function to fetch and display data based on user inputs
def fetch_data(event=None):
    try:
        # Determine the time input: user-specified or current UTC
        if use_current_time.get():
            input_time = datetime.datetime.now(datetime.timezone.utc)
        else:
            user_input = timestamp_input.get()
            input_time = pd.to_datetime(user_input)
            # Set the timezone to UTC
            input_time = input_time.tz_localize("UTC")
            if pd.isnull(input_time):
                # Print that the input is null, so default to current time
                messagebox.showwarning(
                    "Warning",
                    "Invalid timestamp. Defaulting to current UTC time.",
                )
                input_time = datetime.datetime.now(datetime.timezone.utc)

        # Get the dropdown selections
        display_option = dropdown_selection.get()
        angle_unit = angle_unit_selection.get()

        # Get the number of significant figures
        sig_figs = significant_figures_input.get()
        try:
            sig_figs = int(sig_figs)
            if sig_figs <= 0:
                raise ValueError("Significant figures must be greater than 0.")
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid positive integer for significant figures.",
            )
            return

        # Find the closest timestamp in the dataset
        closest_idx = (data["epoch_utc"] - input_time).abs().idxmin()
        row = data.iloc[closest_idx]

        # Clear the table
        for i in table.get_children():
            table.delete(i)

        # Adjust table columns dynamically based on the dropdown selection
        if display_option == "AZ-EL":
            table["columns"] = ("Target", "AZ", "EL")
            table.heading("AZ", text="AZ")
            table.heading("EL", text="EL")
        elif display_option == "RA-Dec":
            table["columns"] = ("Target", "RA", "Dec")
            table.heading("RA", text="RA")
            table.heading("Dec", text="Dec")
        elif display_option == "Both":
            table["columns"] = ("Target", "AZ", "EL", "RA", "Dec")
            table.heading("AZ", text="AZ")
            table.heading("EL", text="EL")
            table.heading("RA", text="RA")
            table.heading("Dec", text="Dec")

        # Set the column width dynamically
        for col in table["columns"]:
            table.column(col, width=100, anchor="center")

        # Check which checkboxes are selected
        selected_keys = []
        for key, var in checkboxes.items():
            if var.get() == 1:
                selected_keys.append(key)

        if not selected_keys:
            messagebox.showwarning("Warning", "No keys selected.")
            return

        # Prepare table data based on dropdown selection and selected keys
        # Add row to the table with alternating row colors
        for idx, key in enumerate(selected_keys):
            az_col = f"az_{key.lower()}"
            el_col = f"el_{key.lower()}"
            ra_col = f"ra_{key.lower()}"
            dec_col = f"dec_{key.lower()}"

            az = round(row[az_col], sig_figs) if az_col in row.index else "N/A"
            el = round(row[el_col], sig_figs) if el_col in row.index else "N/A"
            ra = round(row[ra_col], sig_figs) if ra_col in row.index else "N/A"
            dec = round(row[dec_col], sig_figs) if dec_col in row.index else "N/A"

            # Convert to radians if selected
            if angle_unit == "Radians":
                az = round(np.radians(az), sig_figs) if az != "N/A" else "N/A"
                el = round(np.radians(el), sig_figs) if el != "N/A" else "N/A"
                ra = round(np.radians(ra), sig_figs) if ra != "N/A" else "N/A"
                dec = round(np.radians(dec), sig_figs) if dec != "N/A" else "N/A"

            # Determine row tag (evenrow or oddrow)
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"

            # Insert the row with the correct tag
            if display_option == "AZ-EL":
                table.insert("", "end", values=(key, az, el), tags=(row_tag,))
            elif display_option == "RA-Dec":
                table.insert("", "end", values=(key, ra, dec), tags=(row_tag,))
            elif display_option == "Both":
                table.insert("", "end", values=(key, az, el, ra, dec), tags=(row_tag,))

        # Adjust window size dynamically
        num_rows = len(selected_keys)
        window_height = 600 + min(
            30 * num_rows, 400
        )  # Base height + row-dependent height
        root.geometry(f"800x{window_height}")

        # Update the closest timestamp label
        closest_timestamp_label.config(
            text=f"Closest timestamp found: {row['epoch_utc']}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to handle the "Use Current Time" checkbox
def toggle_current_time():
    if use_current_time.get():
        timestamp_input_field.config(state=DISABLED)
        current_time_label.config(
            text=f"Current UTC Time: {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S}"
        )
    else:
        timestamp_input_field.config(state=NORMAL)
        current_time_label.config(text="")


# Function to toggle all checkboxes
def toggle_checkboxes():
    # Determine if all checkboxes are currently checked
    all_checked = all(var.get() == 1 for var in checkboxes.values())
    # Set all checkboxes to the opposite state
    new_state = 0 if all_checked else 1
    for var in checkboxes.values():
        var.set(new_state)
    fetch_data()  # Fetch data automatically


# Initialize the tkinter GUI
root = Tk()
root.title("LEXI Pointing Data Viewer")
root.geometry("800x600")

# Set the font for the entire GUI
root.option_add("*Font", "Helvetica 12")

# Define a custom style for the left frame
style = ttk.Style()
style.configure(
    "Left.TFrame",
)

# Create the left frame with the custom style
left_frame = ttk.Frame(root, padding=10, style="Left.TFrame")
left_frame.grid(row=0, column=0, sticky="nsew")

right_frame = ttk.Frame(root, padding=10, style="Left.TFrame")
right_frame.grid(row=0, column=1, sticky="nsew")

left_row = 0
right_row = 0
# Configure column weights
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Input field for timestamp
Label(left_frame, text="Enter Timestamp (YYYY-MM-DD HH:MM:SS):").grid(
    row=left_row, column=0, sticky="w", padx=5, pady=5
)
timestamp_input = StringVar()
timestamp_input_field = Entry(right_frame, textvariable=timestamp_input, width=30)
timestamp_input_field.grid(row=right_row, column=1, sticky="E", padx=5, pady=5)
# Add two empty rows for spacing
Label(right_frame, text="").grid(row=right_row + 1, column=1)
Label(right_frame, text="").grid(row=right_row + 2, column=1)
# Label(right_frame, text="").grid(row=right_row + 3, column=1)

# Checkbox to use the current UTC time
use_current_time = IntVar()
# Set the initial state of the checkbox to checked
use_current_time.set(0)

Checkbutton(
    left_frame,
    text="Use Current Time (UTC)",
    variable=use_current_time,
    command=toggle_current_time,
).grid(row=left_row + 1, column=0, sticky="w", padx=5, pady=5)


# Label to display the current UTC time
current_time_label = Label(left_frame, text="", fg="blue")
current_time_label.grid(row=left_row + 2, column=0, sticky="w", padx=5, pady=5)

# Input field for significant figures
Label(left_frame, text="Enter Number of Significant Figures:").grid(
    row=left_row + 3, column=0, sticky="w", padx=5, pady=5
)
significant_figures_input = StringVar(value="2")
Entry(right_frame, textvariable=significant_figures_input, width=10).grid(
    row=right_row + 3, column=1, sticky="E", padx=5, pady=5
)

# Dropdown menu for AZ-EL/RA-Dec/Both selection
Label(left_frame, text="Select Data to Display:").grid(
    row=left_row + 4, column=0, sticky="w", padx=5, pady=5
)
dropdown_selection = StringVar(value="AZ-EL")
dropdown_menu = OptionMenu(
    right_frame, dropdown_selection, "AZ-EL", "RA-Dec", "Both", command=fetch_data
)
dropdown_menu.grid(row=right_row + 4, column=1, sticky="E", padx=5, pady=5)

# Dropdown menu for angle units
Label(left_frame, text="Select Angle Unit:").grid(
    row=left_row + 5, column=0, sticky="w", padx=5, pady=5
)
angle_unit_selection = StringVar(value="Degree")
OptionMenu(
    right_frame, angle_unit_selection, "Degree", "Radians", command=fetch_data
).grid(row=right_row + 5, column=1, sticky="e", padx=5, pady=5)

# Checkboxes for keys
# Label for "Select Targets:"
Label(left_frame, text="Select Targets:").grid(
    row=left_row + 6, column=0, sticky="w", padx=5, pady=5
)

# Creating checkboxes for each target in the keys list
checkboxes = {}
keys = ["Earth", "Sun", "Crab", "Sco", "Mag", "Bonus"]
for i, key in enumerate(keys):
    var = IntVar()
    checkboxes[key] = var
    # Place the checkbox in the second column (column=1) with its label on the left side
    cb = Checkbutton(right_frame, text=key, variable=var, command=fetch_data)
    # Place the checkbox with the label in the second column, aligned to the left by default
    cb.grid(row=right_row + 6 + i, column=1, sticky="E", padx=5, pady=5)

# Set the initial staet of all checkboxes to checked
for var in checkboxes.values():
    var.set(0)

# Button to toggle all checkboxes
Button(left_frame, text="Check/Uncheck All", command=toggle_checkboxes).grid(
    row=left_row + 7, column=0, sticky="w", padx=5, pady=5
)

# Fetch button
Button(left_frame, text="Fetch Data", command=fetch_data, fg="green").grid(
    row=left_row + 9,
    column=0,
    sticky="w",
    padx=5,
    pady=10,
)

# Label to display the closest timestamp
closest_timestamp_label = Label(right_frame, text="", fg="red")
closest_timestamp_label.grid(row=right_row + 12, column=1, padx=5, pady=5)

# Scrollable table for displaying results
table_frame = ttk.Frame(root)
table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Define custom style for the Treeview
style = ttk.Style()
style.theme_use("default")
style.configure(
    "Custom.Treeview",
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white",
    borderwidth=1,
)
style.map("Custom.Treeview", background=[("selected", "#347083")])  # Highlight color

# Apply striped row colors (alternating shades of gray)
style.configure(
    "Custom.Treeview.Heading",
    font=("Helvetica", 14, "bold"),
    background="#f4f4f4",
    foreground="black",
    relief="raised",
)
style.layout(
    "Custom.Treeview.Heading",
    [("Treeheading.cell", {"sticky": "nsew"}), ("Treeheading.text", {"sticky": "ew"})],
)

# Define the font of the table rows and columns other than the headings
style.configure("Custom.Treeview", font=("Helvetica", 12))

table = ttk.Treeview(
    table_frame,
    style="Custom.Treeview",
    show="headings",
    height=10,
)

table.pack(side="left", fill="both", expand=True)
# Set custom tag styles for alternating row colors
table.tag_configure("evenrow", background="#b1babf")
table.tag_configure("oddrow", background="#f7f0f0")

# Get the columns in the table
columns = table["columns"]

print(columns)
# Add scrollbars
vsb = Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
vsb.pack(side="right", fill="y")
hsb = Scrollbar(table_frame, orient=HORIZONTAL, command=table.xview)
hsb.pack(side="bottom", fill="x")

table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Add a button above quit button to clear the table
Button(
    left_frame, text="Clear Table", command=lambda: table.delete(*table.get_children())
).grid(row=left_row + 10, column=0, sticky="w", padx=5, pady=10)
# Quit button
Button(left_frame, text="Quit", command=root.destroy, fg="red").grid(
    row=left_row + 11, column=0, sticky="w", padx=5, pady=10
)

# Run the tkinter event loop
root.mainloop()
