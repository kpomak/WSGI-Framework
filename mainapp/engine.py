from mainapp.models import User, Category, CourseFactory


class Engine:
    def __init__(self):
        self.state = {
            "users": [],
            "categories": {},
        }

    def create_user(self, username):
        user = User(username)
        self.state["users"].append(user)
        return user

    def create_category(self, name, category=None):
        new_category = Category(name)
        if category:
            category.categories[new_category.id] = new_category
        else:
            self.state["categories"][new_category.id] = new_category
        return new_category

    def find_category_by_id(self, id, categories):
        for key, category in categories.items():
            guess = None
            if key == id:
                return category
            if category.categories:
                try:
                    guess = self.find_category_by_id(id, category.categories)
                except Exception:
                    pass
            if guess:
                return guess
        else:
            raise Exception(f"Category {id=} not found")

    def create_course(self, course_type, name, category, **kwargs):
        course = CourseFactory.create(course_type, name, category, **kwargs)
        return course

    def get_course(self, categories, name):
        while name.endswith("_copy"):
            name = name[:-5]
        for category in categories.values():
            for course in category.courses:
                if course.name == name:
                    return course
                if category.categories:
                    course = self.get_course(category.categories, name)
                    if course:
                        return course
        return None
