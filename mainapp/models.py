from copy import deepcopy


class User:
    count = 0

    def __init__(self, username, email, phone):
        self.id = User.count
        User.count += 1
        self.username = username
        self.email = email
        self.phone = phone


class Course:
    def __init__(self, name, category, **kwargs):
        self.name = name
        self.students = []
        self.category = category
        self.category.courses.append(self)

    def clone(self):
        course = deepcopy(self)
        course.name = f"{self.name}_copy"
        course.category = self.category
        self.category.courses.append(course)
        course.students.clear()
        return course


class OfflineCourse(Course):
    def __init__(self, name, category, place=None, **kwargs):
        super().__init__(name, category)
        self.place = place


class OnlineCourse(Course):
    def __init__(self, name, category, platform=None, **kwargs):
        super().__init__(name, category)
        self.platform = platform


class CourseFactory:
    courses = {
        "offline": OfflineCourse,
        "online": OnlineCourse,
    }

    @classmethod
    def create(cls, course_type, name, category, **kwargs):
        return cls.courses[course_type](name, category, **kwargs)


class Category:
    id_counter = 0

    def __init__(self, name):
        self.id = Category.id_counter
        Category.id_counter += 1
        self.name = name
        self.categories = {}
        self.courses = []

    def course_count(self):
        count = len(self.courses)
        if self.categories:
            for category in self.categories.values():
                count += category.course_count()
        return count
