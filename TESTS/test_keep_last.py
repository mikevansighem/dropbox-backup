from dropbox_backup.keep_last import dates_to_utc
from dropbox_backup.keep_last import stale_only

# A dummy backup list of dicts.
dummy_backups_non_naive_non_sorted = [
    {
        'slug': 'd6f0919b',
        'name': 'Automated Backup 2021-12-02',
        'date': '2021-12-02T18:24:31.573701+00:00'
    }, {
        'slug': '599e3f01',
        'name': 'Automated Backup 2020-01-23',
        'date': '2020-01-23T00:00:00.093490+00:00'
    }, {
        'slug': '599e3f01',
        'name': 'Automated Backup 2020-03-05',
        'date': '2020-03-05T00:00:00.073490+00:00'
    }]

# A dummy backup list of dicts with naive dates.
dummy_backups_naive_non_sorted = [
    {
        'slug': 'd6f0919b',
        'name': 'Automated Backup 2021-12-02',
        'date': '2021-12-02T18:24:31.573701'
    }, {
        'slug': '599e3f01',
        'name': 'Automated Backup 2020-01-23',
        'date': '2020-01-23T00:00:00.093490+00:00'
    }, {
        'slug': '599e3f01',
        'name': 'Automated Backup 2020-03-05',
        'date': '2020-03-05T00:00:00.073490'
    }]

# A dummy backup list of dicts with stale backup only
dummy_stale = [
    {
        'slug': '599e3f01',
        'name': 'Automated Backup 2020-01-23',
        'date': '2020-01-23T00:00:00.093490+00:00'
    }]


# Test dates_to_utc from keep_last
class TestDatesToUtc:

    def test_list_type(self):
        result = dates_to_utc(dummy_backups_non_naive_non_sorted)
        assert isinstance(result, list)

    def test_dict_type(self):
        result = dates_to_utc(dummy_backups_non_naive_non_sorted)
        assert isinstance(result[0], dict)

    def test_fix_naive(self):
        result = dates_to_utc(dummy_backups_naive_non_sorted)
        assert result[0]['date'] == '2021-12-02T18:24:31.573701+00:00'


# Test stale_only from keep_last
class TestStaleOnly:

    def test_list_type(self):
        result = stale_only(dummy_backups_non_naive_non_sorted, 2)
        assert isinstance(result, list)

    def test_dict_type(self):
        result = stale_only(dummy_backups_non_naive_non_sorted, 2)
        assert isinstance(result[0], dict)

    def test_sort_and_remove(self):
        result = stale_only(dummy_backups_non_naive_non_sorted, 2)
        assert result == dummy_stale
