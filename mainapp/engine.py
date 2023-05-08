from mainapp.models import User, Category, CourseFactory


class Engine:
    def __init__(self):
        self.state = {
            "users": [],
            "categories": [],
        }

    def create_user(self, username):
        user = User(username)
        self.state["users"].append(user)
        return user

    def create_category(self, name):
        category = Category(name)
        self.state["categories"].append(category)
        return category

    def find_category_by_id(self, id):
        for item in self.state["categories"]:
            if item.id == id:
                return item
        raise Exception(f"Category {id=} not found")

    def create_course(self, course_type, name, category, **kwargs):
        course = CourseFactory.create(course_type, name, category, **kwargs)
        return course

    def get_course(self, name):
        for category in self.state["categories"]:
            for course in category.courses:
                if course.name == name:
                    return course
        return None
