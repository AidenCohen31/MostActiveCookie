import unittest, subprocess,sys,platform,re

platforms = {
    'win32' : "most_active_cookie.bat",
    'linux' : "./most_active_cookie",
    'darwin' : "./most_active_cookie"
}[sys.platform] #selects proper way to run file given a system
class TestCMDLine(unittest.TestCase):
    """
    Tests all invalid command line inputs that are possible
    """
    def test_no_params(self):
        out = subprocess.Popen([platforms], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "Did not input correct parameters")
    def test_bad_csv(self):
        out = subprocess.Popen([platforms, "l", "-d", "2018-1-10"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "path does not exist" )
    def test_bad_date_length(self):
        out = subprocess.Popen([platforms, "cookie_log.csv", "-d", "2018-1"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "invalid date")
    def test_incorrect_date(self):
        out = subprocess.Popen([platforms, "cookie_log.csv", "-d", "2018-13-10"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "month must be in 1..12")
    def test_nonnumeric_date(self):
        out = subprocess.Popen([platforms, "cookie_log.csv", "-d", "a-13-10"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "invalid date")
    def test_no_date(self):
        out = subprocess.Popen([platforms, "cookie_log.csv", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "Did not input correct parameters")
    def test_no_date_flag(self):
        out = subprocess.Popen([platforms, "cookie_log.csv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(out.communicate()[1].decode("utf-8").rstrip(), "'-d' is not in list")

class TestOperations(unittest.TestCase):
    """
    Tests to see if output is right for a specific csv
    """
    def test_all_files(self):
        for i in range(self.numtests):
            out = subprocess.Popen([platforms, "cookie_log.csv", "-d" , self.dates[i]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            msg = max(re.sub(r'\s+', '',out.communicate()[0].decode("utf-8").rstrip()),
            re.sub(r'\s+', '',out.communicate()[1].decode("utf-8").rstrip()),key= lambda x: len(x))
            self.assertEqual(msg, self.answers[i])
    
    def setUp(self):
        """
        sets up testcase data such as dates and expected output
        """
        self.dates = ["2018-12-09","2018-12-08", "2018-12-07", "2018-12-06"]
        self.answers = ["AtY0laUfhglK3lC7","SAZuXPGUrfbcn5UA4sMM2LxV07bPJzwffbcn5UAVanZf6UtG","4sMM2LxV07bPJzwf","No data for date"]
        self.numtests = 4
    
def suite():
    """
    combines all TestCases
    """
    return unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(TestCMDLine),
    unittest.TestLoader().loadTestsFromTestCase(TestOperations)])
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
