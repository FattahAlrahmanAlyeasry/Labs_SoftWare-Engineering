template = """
<h1>مرحبا {name}</h1>
<p>عمرك {age} سنة</p>
"""

student_name = "Fattah"
student_age = 23

html_content = template.format(name=student_name, age=student_age)

with open("student_page.html", "w", encoding="utf-8") as file:
    file.write(html_content)














# students = [
#     {"name": "Ali", "age": 22},
#     {"name": "Sara", "age": 21},
#     {"name": "Mohammed", "age": 23},
# ]

# html_content = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>قائمة الطلاب</title>
# </head>
# <body>
#     <h1>قائمة الطلاب</h1>
#     <ul>
# """

# for student in students:
#     html_content += f"<li>{student['name']} - {student['age']} سنة</li>\n"

# html_content += """
#     </ul>
# </body>
# </html>
# """

# with open("students.html", "w", encoding="utf-8") as file:
#     file.write(html_content)
# # إنشاء صفحة HTML
# html_content = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>صفحة بايثون</title>
# </head>
# <body>
#     <h1>مرحبا بك في صفحة HTML من بايثون!</h1>
#     <p>هذه فقرة ديناميكية.</p>
# </body>
# </html>
# """

# # حفظها في ملف
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(html_content)

# print("تم إنشاء الصفحة بنجاح!")
