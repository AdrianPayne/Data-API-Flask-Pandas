from playbrush_api.brush_stats import week_stats

if __name__ == "__main__":

    raw_path = 'data/1_rawdata.csv'
    group_path = 'data/2_groups.csv'

    with open(raw_path) as raw_csv, open(group_path) as groups_csv:
        user_stats, group_stats = week_stats(raw_csv, groups_csv)

    print('Task 1')
    print(user_stats)
    print('Task 2')
    print(group_stats)
