"""Solution to Hackerrank Challenge 'ANGRY PROFESSOR' https://www.hackerrank.com/challenges/angry-professor"""
DELIMITER = " "


def is_cancelled(number_of_students_present, threshold):
    return threshold > number_of_students_present


def class_size(param):
    result = 0
    for student in param:
        if student <= 0:
            result += 1
    return result


def check_if_class_is_cancelled(first_input, second_input):
    # this splits the input string into two, converts them into integer and assigns the values to the variables
    total_students, threshold = map(int, first_input.strip().split(DELIMITER))
    student_arrivals = map(int, second_input.strip().split(DELIMITER))
    number_of_present_students = class_size(student_arrivals)
    return is_cancelled(number_of_present_students, threshold)

# do the I/O needed for hackerrank.com
if __name__ == '__main__':
    number_of_test_cases = int(raw_input().strip())
    for i in range(number_of_test_cases):
        first_input_line = raw_input()
        second_input_line = raw_input()
        cancelled = check_if_class_is_cancelled(first_input_line, second_input_line)
        if cancelled:
            print "YES"
        else:
            print "NO"
