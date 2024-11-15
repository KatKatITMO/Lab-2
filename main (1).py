import xml.dom.minidom as minidom


DATASET_PATH = "books-en.csv"
TXT_PATH = "20_books.txt"
XML_PATH = "currency.xml"


def get_n_line(dataset, number):
    line = ""
    dataset.seek(0)
    for i in range(number):
        line = next(dataset)
    return line


def str_to_list(string=""):
    ans = string
    ans = ans.replace("&amp;", "&")
    ans = ans.replace("&lt;", "<")
    ans = ans.replace(" ; ", "#@!_lr")
    ans = ans.replace(" ;", "#@!_left")
    ans = ans.replace("; ", "#@!_right")
    ans = ans.replace(",0", ".0")
    ans = ans.replace(",1", ".1")
    ans = ans.replace(",2", ".2")
    ans = ans.replace(",3", ".3")
    ans = ans.replace(",4", ".4")
    ans = ans.replace(",5", ".5")
    ans = ans.replace(",6", ".6")
    ans = ans.replace(",7", ".7")
    ans = ans.replace(",8", ".8")
    ans = ans.replace(",9", ".9")
    ans = ans.split(';')
    for item in ans:
        item = item.replace("#@!_lr", " ; ")
        item = item.replace("#@!_left", " ;")
        item = item.replace("#@!_right", "; ")
    return ans


def count_headers_longer_30_sym(dataset):
    ans = 0
    line = get_n_line(dataset, 2)
    while line != "END_OF_DOC":
        listed = str_to_list(line)
        if len(listed[1]) > 30:
            ans += 1
        line = next(dataset, "END_OF_DOC")
    print(ans)


def author_finder(dataset, author_name, price):
    dataset.seek(0)
    line = next(dataset)
    while line != "END_OF_DOC":
        listed = str_to_list(line)
        if listed[2].find(author_name) != -1:
            if float(listed[6]) <= price:
                print(listed[0], listed[1])
        line = next(dataset, "END_OF_DOC")


def generator(dataset):
    with open(TXT_PATH, 'w') as txt_file:
        to_the_txt = ""
        line = get_n_line(dataset, 4851)
        for i in range(20):
            listed = str_to_list(line)
            to_the_txt += (
                f"{4851 + i}: {listed[2]}. {listed[1]} - {listed[3]}\n")
            line = next(dataset)
        txt_file.write(to_the_txt)


def xml():
    with open(XML_PATH, "r", encoding="UTF-8") as xml_file:
        xml_data = xml_file.read()

        dom = minidom.parseString(xml_data)
        dom.normalize()

        elements = dom.getElementsByTagName('Valute')
        dict_for_xml = {}

        for node in elements:
            CharCode = ""
            NumCode = ""
            for child in node.childNodes:
                if child.nodeType == 1:
                    if child.tagName == 'CharCode':
                        if child.firstChild.nodeType == 3:
                            CharCode = str(child.firstChild.data)
                    if child.tagName == 'NumCode':
                        if child.firstChild.nodeType == 3:
                            NumCode = int(child.firstChild.data)
                dict_for_xml[NumCode] = CharCode
        dict_for_xml.pop('')
        print(dict_for_xml)


def create_list(count, default_value):
    created_list = []
    for i in range(count):
        created_list.append(default_value)
    return created_list


def add_into_list(cur_list=list, value=list):
    ans_list = cur_list
    for i in range(len(ans_list)):
        if int(ans_list[i][0]) <= int(value[0]):
            ans_list.insert(i, value)
            ans_list.pop()
        break
    return ans_list


def most_popular_20_books(dataset):
    ans = create_list(20, [-1, ""])
    line = get_n_line(dataset, 2)
    while line != "END_OF_DOC":
        listed = str_to_list(line)
        ans = add_into_list(ans, [listed[5], listed[1]])
        line = next(dataset, "END_OF_DOC")

    for item in ans:
        print(item[1] + " (Downloads: " + str(item[0]) + ")")


def list_of_publishers(dataset):
    line = get_n_line(dataset, 1)
    line = next(dataset, "END_OF_DOC")
    set_of_publishers = set()
    while line != "END_OF_DOC":
        set_of_publishers.add(str_to_list(line)[4])
        line = next(dataset, "END_OF_DOC")
    ans = list(set_of_publishers)
    ans.sort()
    print(ans)
    same_item_checker(ans)


def same_item_checker(cur_list=list):
    if len(cur_list) == 1:
        print("Nice!")
    for i in range(len(cur_list) - 1):
        if cur_list[i] == cur_list[i + 1]:
            print("ERROR SAME_ITEM_CHECKER")


if __name__ == "__main__":
    with open(DATASET_PATH, encoding="Latin-1") as dataset:
        count_headers_longer_30_sym(dataset)
        author_finder(dataset, " ", 20)
        generator(dataset)
        xml()
        most_popular_20_books(dataset)
        list_of_publishers(dataset)
