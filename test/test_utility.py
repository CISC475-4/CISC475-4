import sys
import utility.file_utility as file_utility

from nose.tools import (assert_raises, assert_tuple_equal, assert_list_equal)

#test xls_to_csv
good_fn = "test/test_data/UtilityTestData_.xlsx"
fake_fn = "lego_building_block_chart.xlsx"

def test_xls_to_csv():
    print "testing xls_to_csv in file_utility.py"
    #assert_raises(IOError, file_utility.xls_to_csv, fake_fn)
    assert_tuple_equal(file_utility.xls_to_csv(good_fn), 
      ('UtilityTestData_AllGroupData.csv', 'UtilityTestData_TimeSeriesData.csv')
    )

#test getDataFrom
good_csv = "test/test_data/UtilityTestData_TimeSeriesData.csv"
fake_csv = "chromatic_lego_color_chart_by_time_of_day.csv"

time_series_header = [
    'TIME [SEC]', 'BEHAV 1', 'BEHAV 1 LEVEL', 'BEHAV 2', 
    'BEHAV 2 LEVEL', 'BEHAV 3', 'BEHAV 3 LEVEL', 'COMBO', 'COMBO LEVE'
]

time_series_values = [
    {
        'TIME [SEC]': '0.333333333333', 
        'BEHAV 3': 'Ver_(quiet)', 
        'BEHAV 2': 'Aff_(interest)', 
        'BEHAV 1': 'Att_(trainer)', 
        'BEHAV 2 LEVEL': '3', 
        'BEHAV 3 LEVEL': '0', 
        'BEHAV 1 LEVEL': '5', 
        'COMBO': 'Att_(trainer):Aff_(interest):Ver_(quiet)', 
        'COMBO LEVE': '53'
    }
]

def test_get_data_from_csv():
   print "testing get_data_from_csv in file_utility.py"
   testRetrieval  = file_utility.get_data_from_csv(good_csv)
   
   assert_list_equal(testRetrieval[0], time_series_header)
   assert_list_equal(testRetrieval[1], time_series_values)
   assert_raises(IOError, file_utility.get_data_from, fake_csv)

test_xls_to_csv()
test_get_data_from()
