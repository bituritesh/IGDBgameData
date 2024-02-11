from gameGenrePredictor import igdb_scrapper
from sheetWriter import genre_appender_in_gsheet


# Reading sheet url col
def gsheet_url_reader(worksheet):
    genre_list = []
    column_to_read = 4
    # Read values from the chosen column until the last non-empty cell
    igdb_link_list = worksheet.col_values(column_to_read)[1:]  # Skip the first row (header)
    print(f"First Link  - {igdb_link_list[0]},Last Link -{igdb_link_list[len(igdb_link_list)-1]}")
    print("^"*60)
    print(f'total length of the extracted data from gsheet - {len(igdb_link_list)}')
    genre_list.append(genre_extractor(igdb_link_list, worksheet))
    print(genre_list)


def reading_the_last_data_in_genre_column(sheet_to_be_read):
    all_genre_values = sheet_to_be_read.col_values(sheet_to_be_read.find('genre').col)
    genre_column_length = len(all_genre_values) - all_genre_values.count('')  # Exclude empty cells from count
    column_no = sheet_to_be_read.find('url').col
    row_to_fetch = genre_column_length  # Fetch value at the determined length
    url_cell_value = sheet_to_be_read.cell(row_to_fetch, column_no).value
    print(f"URL - {url_cell_value} already updated with genre")
    return url_cell_value


def genre_extractor(igdb_web_urls, worksheet):
    last_updated_genre_cell_value_url = reading_the_last_data_in_genre_column(worksheet)
    if last_updated_genre_cell_value_url in igdb_web_urls:
        position = igdb_web_urls.index(last_updated_genre_cell_value_url)  # Get the index of 'url'
        print(f"{last_updated_genre_cell_value_url} found at position: {position+2} in gsheet")
        next_url_in_gsheet = position + 1
        for link in igdb_web_urls[next_url_in_gsheet:]:
            result = []
            print("-" * 70)
            print(link)
            genre = igdb_scrapper(link)
            string_genre_list = [str(item) for item in genre]
            # Define the substring to search for
            substring = "genres"
            # Iterate through the list
            for item in string_genre_list:
                if substring in item:
                    split_by_genres = item.split('/genres/')[1:]
                    for final_item in split_by_genres:
                        start = final_item.find('">')  # Find the start index of the substring
                        end = final_item.find('</a>')  # Find the end index of the substring
                        if start != -1 and end != -1:
                            substring = final_item[start + 2:end]  # Extract the substring between '">' and '</a>'
                            result.append(substring.strip())
                else:
                    result.append("-")
            print("printing this {}".format(result))  # here data will be appended to the same gsheet mapped with url
            genre_appender_in_gsheet(genre_each_game=result, genre_sheet=worksheet)
        return result
    else:
        print(f"{'!'*50}{last_updated_genre_cell_value_url} not found in the list")
