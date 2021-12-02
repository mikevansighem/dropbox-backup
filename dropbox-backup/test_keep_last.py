import pytest

from keep_last import dates_to_utc

# A dummy backup list of dicts with only UTC values.
dummy_backups_all_utc = [
    {'slug': 'd6f0919b', 'name': 'Automated Backup 2021-12-02', 'date': '2021-12-02T18:24:31.573701+00:00'},
    {'slug': '599e3f01', 'name': 'Automated Backup 2021-12-01', 'date': '2021-12-01T00:00:00.093490+00:00'}
    ]

class TestDatesToUtc:
    """ Test dates_to_utc from keep_last """

    def test_for_no_change(self):
        assert dates_to_utc(dummy_backups_all_utc) == dummy_backups_all_utc

    def test_list_type(self):
        result = dates_to_utc(dummy_backups_all_utc)
        assert isinstance(result, list)

    def test_dict_type(self):
        result = dates_to_utc(dummy_backups_all_utc)
        assert isinstance(result[0], dict)
