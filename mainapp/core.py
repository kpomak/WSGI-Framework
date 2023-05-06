from copy import deepcopy
from datetime import datetime


class User:
    def __init__(self, username):
        self.username = username



class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def clone(self):
        return deepcopy(self)


class OfflineCourse(Course):
    def __init__(self, name, category, place):
        super().__init__(name, category)
        self.place = place


class OnlineCourse(Course):
    def __init__(self, name, category, platform):
        super().__init__(name, category)
        self.platform = platform


class CourseFactory:
    courses = {
        'offline': OfflineCourse,
        'online': OnlineCourse,
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
        self.courses = []

    def course_count(self):
        return len(self.courses)


class Engine:
    def __init__(self):
        self.users = []
        self.courses = []
        self.categories = []


    def create_user(self, username):
        user = User(username)
        self.users.append(user)
        return user


    def create_category(self, name):
        category = Category(name)
        self.categories.append(category)
        return category

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Category {id=} not found')

    @staticmethod
    def create_course(course_type, name, category, **kwargs):
        return CourseFactory.create(course_type, name, category, **kwargs)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None


class BaseLogger(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=BaseLogger):
    def __init__(self, name):
        self.name = name

    def log(self, message):
        with open(f'./var/log/{self.name}.log', 'a', encoding='utf-8') as f:
            f.write(f'[{datetime.now()}] : {message}')
