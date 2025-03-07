import glob

import pandas as pd


def get_lexi_look_direction_data():
    # Get all the files in the directory
    files = glob.glob("../data/LEXI_gimbal_pointing_values/LEXI_Pointing_Measured*.csv")

    print(f"Found {len(files)} files")
    # Create an empty dataframe
    df_list = []

    # Loop through all the files
    for file in files:
        # Read the file
        data = pd.read_csv(file, skiprows=1)

        # Append the data to the list
        df_list.append(data)

    # Concatenate the data
    df = pd.concat(df_list)

    df.columns = ["epoch_utc", "dec_lexi", "ra_lexi"]

    # Remove the degree symbol
    df["dec_lexi"] = df["dec_lexi"].str.replace("°", "").astype(float)
    df["ra_lexi"] = df["ra_lexi"].str.replace("°", "").astype(float)
    # Set the time zone to UTC
    df["epoch_utc"] = pd.to_datetime(df["epoch_utc"], utc=True)
    df = df.set_index("epoch_utc")
    # Sort the data
    df = df.sort_index()

    # Check for duplicate indices
    # df = df[~df.index.duplicated(keep="first")]

    return df


if __name__ == "__main__":
    # Get the data
    lexi_df = get_lexi_look_direction_data()

    start_time = "2025-03-02 12:00:00"
    start_time = pd.to_datetime(start_time, utc=True)

    # Shift the index by the time difference between the first time in the data and the start time
    lexi_df.index = lexi_df.index - (lexi_df.index[0] - start_time)

    # Save the data
    lexi_df.to_csv("../data/lexi_look_direction_data.csv", index=True)


lexi_df = pd.read_csv("../data/lexi_look_direction_data.csv")
#  Sed epoch_utc to datetime
lexi_df["epoch_utc"] = pd.to_datetime(lexi_df["epoch_utc"])

# Set epoch_utc as the index
lexi_df = lexi_df.set_index("epoch_utc")


# Load the CSV file
data = pd.read_csv("../data/LEXIAngleData_20250304.csv")
data["epoch_utc"] = pd.to_datetime(data["epoch_utc"])
# Set the timezones to UTC
data["epoch_utc"] = data["epoch_utc"].dt.tz_localize("UTC")

# Set the index to the epoch_utc
data = data.set_index("epoch_utc")
# Record the start time of the GUI

# Reset the index for both dataframes
# data = data.reset_index()
#
# lexi_df = lexi_df.reset_index()

df_merged = pd.merge(data, lexi_df, on="epoch_utc", how="outer")
# Merge the two dataframes
# merged_df = pd.merge_asof(
#     lexi_df,
#     data,
#     left_index=True,
#     right_index=True,
#     tolerance=pd.Timedelta("1min"),
#     direction="nearest",
# )

# Set the index to the epoch_utc
# df_merged = df_merged.set_index("epoch_utc")

# Save the data
df_merged.to_csv("../data/merged_lexi_look_direction_data_20250306.csv", index=True)
