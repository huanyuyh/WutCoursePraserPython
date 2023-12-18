from bs4 import BeautifulSoup
import csv

def save_courses_to_csv(courses, filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Day", "Position", "Teacher", "Start Node", "End Node", "Start Week", "End Week", "Note", "Credit", "Extra1", "Extra2"])
        for course in courses:
            writer.writerow([course.name, course.day, course.position, course.teacher, course.start_node, course.end_node, course.start_week, course.end_week, course.note, course.credit, course.extra1, course.extra2])

def load_courses_from_csv(filename):
    courses = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            if row:  # 确保行不是空的
                course = Course(*row)
                courses.append(course)
    return courses
class Course:
    def __init__(self, name, day, position, teacher, start_node, end_node, start_week, end_week, note,credit="",  extra1="", extra2=""):
        self.name = name
        self.day = day
        self.position = position
        self.teacher = teacher
        self.start_node = start_node
        self.end_node = end_node
        self.start_week = start_week
        self.end_week = end_week
        self.credit = credit
        self.note = note
        self.extra1 = extra1
        self.extra2 = extra2

    def __str__(self):
        return f"{self.name} {self.day} {self.position} {self.teacher} {self.start_node} {self.end_node} {self.start_week} {self.credit}"

class CourseInfo:
    def __init__(self, name, day, position, time, note):
        self.name = name
        self.day = day
        self.position = position
        self.time = time
        self.note = note
    def __str__(self):
        return f"{self.name} {self.day} {self.position} {self.time}{self.note}"

def parse_course_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    element_with_id = soup.find(id="xqkb")

    if element_with_id:
        # print("Element with id 'xqkb':", element_with_id)
        table = element_with_id.find('table')
        rows = table.find_all('tr')

        # 第一行通常包含星期的标题
        weekdays = [th.get_text() for th in rows[0].find_all('th')]
        courseInfoList = list()
        # 遍历剩下的行来提取课程信息
        for row in rows[1:]:
            isMoreOneColumn = False  #因为上午下午两个文字导致多了一行
            for i, cell in enumerate(row.find_all('td')):
                cellStr = str(cell)
                if(i==0):
                    if(cellStr.find("午")>0 or cellStr.find("晚")>0):
                        isMoreOneColumn = True
                    else:
                        isMoreOneColumn = False
                    # print(i)
                    # print(str(cell))
                # if(i==1):
                #     # print(i)
                #     #print(str(cell))
                #     if(cellStr.find("target=\"_blank\">")>0):
                #         name = cellStr[cellStr.find("target=\"_blank\">")+len("target=\"_blank\">"):cellStr.find("<p>")]
                #         print(name)
                #         if(not isMoreOneColumn):
                #             weekDay = i
                #             print("周"+str(weekDay))
                else:
                    #print(i)
                    # print(str(cell))
                    while (cellStr.find("target=\"_blank\">") > 0):
                        name = cellStr[
                               cellStr.find("target=\"_blank\">") + len("target=\"_blank\">"):cellStr.find("<p>")]
                        name = name.replace("\n","").replace(" ","").replace("\t","")
                        #print(name)
                        cellStr = cellStr[cellStr.find("<p>")+len("<p>"):]
                        position = cellStr[:cellStr.find("</p>")]
                        #print(position)
                        cellStr = cellStr[cellStr.find("</p>") + len("</p>"):]
                        times = cellStr[cellStr.find("<p>")+len("<p>"):cellStr.find("</p>")]
                        #print(times)
                        cellStr = cellStr[cellStr.find("</p>") + len("</p>"):]
                        # print(cellStr)
                        cellTempHaveNote = cellStr[:cellStr.find("</a>")]
                        if (isMoreOneColumn):
                            weekDay = i-1
                            #print("周" + str(weekDay))
                        else:
                            weekDay = i
                            #print("周" + str(weekDay))
                        if(cellTempHaveNote.find("<p>")>0):
                            note = cellTempHaveNote[cellTempHaveNote.find("<p>")+len("<p>"):cellTempHaveNote.find("</p>")]
                            #print(note)
                            cellStr = cellStr[cellStr.find("</div>"):]
                            courseInfo = CourseInfo(name,weekDay,position,times,note)
                            courseInfoList.append(courseInfo)
                        else:
                            courseInfo = CourseInfo(name, weekDay, position, times, "")
                            courseInfoList.append(courseInfo)
        courseList = list()
        weekDaySet = {1:"周一",
                      2:"周二",
                      3:"周三",
                      4:"周四",
                      5:"周五",
                      6:"周六",
                      7:"周日"}
        for courseInfo in courseInfoList:
            print(courseInfo)
            tempStr = courseInfo.time
            temNodes = str(tempStr)[str(tempStr).find("("):].replace("(","").replace("节)","")
            temNodes = (str(temNodes).split("-"))
            print(temNodes)
            start_node = temNodes[0]
            stop_node = temNodes[1]
            print(start_node+"-"+stop_node)
            temWeeks = str(tempStr)[:str(tempStr).find("(")].replace("◇第","").replace("周","")
            temWeeks = str(temWeeks).split(",")
            for weeks in temWeeks:
                temp = str(weeks).split("-")
                start_week = temp[0]
                stop_week = temp[1]
                print(temp)
                course = Course(courseInfo.name,courseInfo.day,courseInfo.position,"",int(start_node),int(stop_node),int(start_week),int(stop_week),courseInfo.note)
                courseList.append(course)


        teacherInfos = soup.find('div',class_="table-inner table-long table-renwu")
        tableInfos = teacherInfos.find('table')
        # print(tableInfos)
        rows = tableInfos.find_all('tr')
        print("开始")
        for row in rows[2:]:
            print("开始1")
            name = ""
            teacher = ""
            credit = ""
            for i, cell in enumerate(row.find_all('td')):
                tempStr = cell.get_text()
                if(i==0):
                    name = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==1:
                    credit = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==2:
                    qq = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==3:
                    weeks = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==4:
                    teacher = str(tempStr).replace("\n","").replace(" ","").replace("\t","")
                elif i==5:
                    for course in courseList:
                        if(course.name == name):
                            course.teacher = teacher
                            course.credit = credit
        for course in courseList:
            print(course)
        save_courses_to_csv(courseList, "courses.csv")







                    # weekday = weekdays[i]
                    # weekdayInfo = str(weekday).replace("\n", "").replace("\t", "")
                    # weekdayInfo = weekdayInfo.replace(" ", "")
                    # course_info = cell.get_text()
                    # if course_info.strip():
                    #     name = ""
                    #     day = ""
                    #     position = ""
                    #     start_node = ""
                    #     end_node = ""
                    #     start_week = ""
                    #     end_week = ""
                    #     note = ""
                    #     # print(
                    #     #     f"1上课时间: {weekdayInfo}")
                    #     # print(cell)
                    #     texts = cell.get_text(separator='|').split('|')
                    #     # print(texts)
                    #     num = -1
                    #     for text in texts:
                    #
                    #         if(len(text)>1):
                    #             num = num + 1
                    #             tempStr = text.strip().replace("\n", "").replace("\t", "")
                                # print(tempStr)
                                # print(num)
                                # if num == 0:
                                #     name = str(tempStr)
                                #     print(name)
                                # elif num ==1:
                                #     position = str(tempStr).replace("@","")
                                #     print(position)
                                # elif num ==2:
                                #     temNodes = str(tempStr)[str(tempStr).find("("):].replace("(","").replace("节)","")
                                #     temNodes = (str(temNodes).split("-"))
                                #     start_node = temNodes[0]
                                #     stop_node = temNodes[1]
                                #     print(start_node+"-"+stop_node)
                                #     temWeeks = str(tempStr)[:str(tempStr).find("(")].replace("◇第","").replace("周","")
                                #
                                #     temWeeks =(str(temWeeks).split(","))
                                #     for temWeek in temWeeks:
                                #         temWeek = temWeek.split("-")
                                #         # print(temWeek)
                                #         start_week = temWeek[0]
                                #         stop_week = temWeek[1]
                                #         print(start_week+"-"+stop_week)
                                # elif num ==3:
                                #     print("name"+name)
                                #     if(str(tempStr).find(name[1:])>0):
                                #
                                #         print("yes")
                                #     # if(str(tempStr))
                                #     print(tempStr)
                                # elif num == 4:
                                #     print(tempStr)
                                # elif num == 5:
                                #     print(tempStr)
                                # elif num == 6:
                                #     print(tempStr)
                                # elif num == 7:
                                #     print(tempStr)
                                # elif num == 8:
                                #     print(tempStr)
                                # elif num == 9:
                                #     print(tempStr)

                # print(cell.find_all('a'))
                # if course_info.strip():  # 如果单元格有课程信息
                #     weekday = weekdays[i]
                #     courseInfo = str(course_info)
                #     courseInfo = courseInfo.replace("\n","").replace("\t", "")
                #     courseInfo = courseInfo.replace(" ", "")
                #     weekdayInfo = str(weekday).replace("\n","").replace("\t", "")
                #     weekdayInfo = weekdayInfo.replace(" ", "")
                    # print(
                    #     f"课程信息: {courseInfo}, "
                    #       f"上课时间: {weekdayInfo}")
        # for row in table.find_all('tr'):
        #     for cell in row.find_all('td'):
        #         # 获取链接
        #         link = cell.find('a')['href'] if cell.find('a') else "No Link"
        #         # 获取文本内容
        #         texts = cell.get_text(separator='|').split('|')
        #         # 打印提取的信息
        #         print(f"Link: {link}")
        #         for text in texts:
        #             print(text.strip())
        with open("./test.txt", 'w', encoding='utf-8') as file:
            file.write(element_with_id.text)
    else:
        print("No element with id 'xqkb' found.")

# 测试代码
# file_path = f"C:/Users/HUANYU/Downloads/jwc.htm"  # 替换为你的 HTML 文件路径
# parse_course_html(file_path)
