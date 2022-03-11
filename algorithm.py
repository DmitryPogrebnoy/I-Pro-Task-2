import re
import datetime
import statistics


def process_line(line):
    # Обработка входящщих строк

    line = line.strip()
    data = re.split('\s+', line)
    date = data[0].split(sep=".")
    time = data[1].split(sep=":")

    ## (weekday, hours, minutes, traffic_value)
    clean_data = (
        datetime.datetime(year=int(date[2]), month=int(date[1]), day=int(date[0])).weekday(), int(time[0]),
        int(time[1]),
        float(data[5]))

    return clean_data


WINDOW_SIZE = 4


def get_history_weighted_mean(history, day, hours, minutes):
    # Вычисляет среднее взвешенное историческое значение
    # Здесь можно было бы использовать datetime, но я не успел, поэтому так :)
    day_hour_history = history[(day, hours)]

    if hours == 0:
        if day == 0:
            before_hour_day = 7
            before_hour_hour = 23
        else:
            before_hour_day = day - 1
            before_hour_hour = 23
    else:
        before_hour_day = day
        before_hour_hour = hours - 1

    day_before_hour_history = history[(before_hour_day, before_hour_hour)]

    return day_before_hour_history[3] * (1 - minutes / 60) + day_hour_history[3] * (minutes / 60)


def compute_new_metric(history, current_data, line):
    # Определяет является ли новое значение повышенным или пониженным
    processed_line = process_line(line)
    current_data.append(processed_line)
    if len(current_data) >= WINDOW_SIZE:
        last_values = [value[3] for value in current_data[-WINDOW_SIZE:]]
        mean_current_value = statistics.mean(last_values)
        mean_history_value = get_history_weighted_mean(history, processed_line[0], processed_line[1],
                                                       processed_line[2])
        print(mean_current_value)
        print(mean_history_value * 1.3)
        print(mean_history_value * 0.9)
        if mean_current_value > mean_history_value * 1.3:
            print("Трафик выше нормы")
        elif mean_current_value < mean_history_value * 0.9:
            print("Tрафик ниже нормы")
        else:
            print("Tрафик в норме")


def main():
    # Читайм и заполняем исторические данные
    history = {}
    with open("history.txt") as f:
        for line in f.readlines():
            processed_line = process_line(line)
            history[(processed_line[0], processed_line[1])] = processed_line

    current_data = list(tuple())

    # Обрабатываем ввод
    line = input('Enter "File" for run example or enter "Data" for add new data:')
    if line == "Exit":
        exit()
    elif line == "File":
        with open("new.txt") as f:
            for line in f.readlines():
                compute_new_metric(history, current_data, line)
    else:
        while True:
            line = input('Enter new data:')
            if line == "Exit":
                exit()
            
            compute_new_metric(history, current_data, line)


if __name__ == "__main__":
    main()
