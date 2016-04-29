import unittest

from main.angry_professor import is_cancelled, class_size, check_if_class_is_cancelled


class AngryProfessorTest(unittest.TestCase):
    def test_forThresholdZero_classIsNotCancelled(self):
        cancelled = is_cancelled(0, 0)
        self.assertFalse(cancelled)

    def test_forThresholdOne_emptyClassIsCancelled(self):
        cancelled = is_cancelled(0, 1)
        self.assertTrue(cancelled)

    def test_forListOfArrivalTimes_classSizeIsNumberOfNotPositives(self):
        size = class_size([-2, -1, 0, 1, 2])
        self.assertEquals(3, size)

    def test_forListOfArrivalTimes_classSizeIsNumberOfNotPositives2(self):
        size = class_size([-2, 1, 0, 2])
        self.assertEquals(2, size)

    def test_specifiedInputFormat(self):
        result = check_if_class_is_cancelled("4 3", "0 -3 -4 2")
        self.assertFalse(result)
