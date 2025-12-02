from datetime import datetime, timezone
def extract_data(file_name: str) -> list[tuple[int, str, str, datetime, float, float, float, float, float, float]]:
    values = []
    with open(file_name) as file:
        content = file.read()
    content = content.split("\n")
    for i in range(1, len(content) - 1):
        row_content = content[i].split(",")
        print(row_content)
        dt = datetime.strptime(row_content[3], "%Y-%m-%d %H:%M:%S")
        dt_utc = dt.replace(tzinfo=timezone.utc)
        time_date = dt_utc.isoformat().replace('+00:00', "Z")
        values.append((int(row_content[0]), row_content[1], row_content[2], time_date, row_content[4], row_content[5], row_content[6], row_content[7], row_content[8], row_content[9]))

    return values
