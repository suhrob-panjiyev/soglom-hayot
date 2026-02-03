def calc_bmr(age, sex, weight, height):
    if sex == "erkak":
        return 10*weight + 6.25*height - 5*age + 5
    return 10*weight + 6.25*height - 5*age - 161


def calc_tdee(bmr, activity):
    return bmr * activity


def adjust_for_goal(tdee, goal):
    if goal == "ozish":
        return tdee - 400
    elif goal == "semirish":
        return tdee + 400
    return tdee


def calc_macros(calories, weight):
    protein = 1.6 * weight
    fat = 0.8 * weight
    carbs = (calories - (protein*4 + fat*9)) / 4
    return protein, fat, carbs
