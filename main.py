from IGDBGenreScrapper import gsheet_url_reader
from sheetWriter import connecting_to_worksheet, receive_data_from_igdb_api
from gameGenrePredictor import game_data_for_id


def genre_scrapper_logic(worksheet):
    print("Nice👌")
    gsheet_url_reader(worksheet)


def gsheet_game_details_collector(gsheet_to_be_written):
    gsheet_last_updated_game_id = 0
    # Writing games data to sheet
    # Define headers
    headers = ["id", "name", "storyline", "url", "genre"]
    last_row_index = len(gsheet_to_be_written.col_values(1))  # column A has continuous data
    # to check the sheets last entry is greater than 1, then pick the last entry of column 1 else push the headers
    if gsheet_to_be_written.row_values(1) == headers and last_row_index > 1:
        # Get the values of the last row
        last_row_values = gsheet_to_be_written.row_values(last_row_index)
        gsheet_last_updated_game_id = int(last_row_values[0])
        print(f"Last row data: {last_row_values}")
    else:
        # Write headers to the sheet if sheet is empty, Insert at the first row
        print("The sheet is empty. Inserting headers")
        gsheet_to_be_written.insert_row(headers, index=1)

    # calling game_data_for_id() from gameGenrePredictor.py to update the gsheet data
    data_received, total_length = game_data_for_id(gsheet_last_updated_game_id + 1)  # received the full data
    receive_data_from_igdb_api(data_received, total_length, gsheet_to_be_written)


if __name__ == "__main__":
    sheet_to_be_written = sheet_to_be_read = connecting_to_worksheet()
    # Running genre scrapper below >
    #genre_scrapper_logic(sheet_to_be_read)
    # collecting game information from IGDB games API below >
    gsheet_game_details_collector(sheet_to_be_written)


