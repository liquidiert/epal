import sys
import re
import os


def epal_parser():
    args = sys.argv[1:]
    vars = []
    with open(str(args[0]), 'r') as parse_file:
        cpp_output = str(args[0]).split(".")
        with open(cpp_output[0] + ".cpp", 'w+') as parsed_file:
            parsed_file.write("#include <iostream>\nusing namespace std;\n")
            print_case = False
            in_loop = False
            if_case = False
            switch = False
            pre_line = None
            block_comment = False
            block_comment_index = 0
            class_declaration = False
            end_string = False
            current_tabs = 0
            for line in parse_file:
                index = 0
                line = line.split()
                if block_comment:
                    if "end" in line:
                        parsed_file.write("*/\n")
                        block_comment = False
                        break
                    elif block_comment_index == 1:
                        comments = " ".join(line[1:])
                        parsed_file.write(comments + "\n")
                        block_comment_index += 1
                    else:
                        comments = " ".join(line)
                        parsed_file.write(comments + "\n")
                        block_comment_index += 1

                else:
                    for word in line:
                        if re.match("[0-9]", word):  # special characters section
                            if not in_loop:
                                value = word
                                parsed_file.write(value + ";\n")
                            elif line[index - 1] == "+" or line[index - 1] == "add" and if_case:
                                value = word
                                parsed_file.write(value + ";\n")
                            index += 1
                        elif ' ' in line:
                            if len(line) > 3:
                                if line[index - 1] == " " or line[index + 1] == " ":
                                    current_tabs += 1
                            else:
                                current_tabs += 1
                            index += 1
                        elif word == "class":  # class section
                            if not len(line[2:]) == 0:
                                class_args = "(" + str(line[2:]) + ")"
                            else:
                                class_args = ""
                            parsed_file.write("class " + line[index + 1] + " " + class_args + " {\n")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            parsed_file.write("private:\n")  # classes are per default private
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            class_declaration = True
                            index += 1
                            break
                        elif word == "public":
                            for i in range(current_tabs):
                                parsed_file.write("\t")
                            parsed_file.write("\npublic:\n")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            index += 1
                        elif word == "main":  # main section
                            parsed_file.write("int main() {\n")
                            index += 1
                        elif word == "is" or word == "=":  # operators
                            parsed_file.write(" = ")
                            index += 1
                        elif word == "add" or word == "+":
                            parsed_file.write(" + ")
                            index += 1
                        elif word == "sub" or word == "-":
                            parsed_file.write(" - ")
                            index += 1
                        elif word == "mul" or word == "*":
                            parsed_file.write(" * ")
                            index += 1
                        elif word == "div" or word == "/":
                            parsed_file.write(" / ")
                            index += 1
                        elif word == "mod" or word == "%":
                            if not if_case:
                                parsed_file.write(" % ")
                            index += 1
                        elif word == "equals" or word == "==":
                            if not if_case:
                                parsed_file.write(" == ")
                            index += 1
                        elif word == "nequal" or word == "!=":
                            parsed_file.write(" != ")
                            index += 1
                        elif word == "and" or word == "&&":
                            parsed_file.write(" && ")
                            index += 1
                        elif word == "or" or word == "||":
                            parsed_file.write("||")
                            index += 1
                        elif word == "end":
                            if switch:
                                switch = False
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                                parsed_file.write('default:\n\tcout << "Switch case error" << endl;\n}')
                            elif class_declaration:
                                class_declaration = False
                                parsed_file.write("};\n")
                            else:
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                                parsed_file.write("}\n")
                            current_tabs = 0
                            in_loop = False
                            if_case = False
                            index += 1
                        elif word == "do":  # useless words
                            index += 1
                            pass
                        elif word == "for":
                            index += 1
                        elif word == "in":
                            index += 1
                        elif word == "range":
                            index += 1
                        elif word == "loop":  # loop section
                            variable_name = line[index + 2]
                            if "for" in line:
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                                parsed_file.write("for (int " + variable_name + " = 0; " + variable_name
                                                  + " < " + line[index + 5] + "; " + variable_name + "++) {\n")
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                            else:
                                for i in range((current_tabs/4)):
                                    parsed_file.write("\t")
                                parsed_file.write("\nwhile (" + variable_name + " < " + line[index + 5] + "{\n")
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                            in_loop = True
                            index += 1
                            break
                        elif word == "if":  # if section
                            if_case = True
                            conditions = " ".join(line[1:])
                            conditions = conditions.replace("equals", " == ")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            parsed_file.write("if (")
                            parsed_file.write(conditions)
                            parsed_file.write(") {\n")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            index += 1
                            break
                        elif word == "else":
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            parsed_file.write("else {\n")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            index += 1
                        elif word == "elif":
                            conditions = " ".join(line[1:])
                            conditions = conditions.replace("equals", " == ")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            parsed_file.write(" else if (" + conditions + ") {\n")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            index += 1
                        elif word == "print":  # builtins
                            if line[index + 1] in vars:
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                                parsed_file.write("cout << " + line[index + 1] + " << endl;\n")
                            else:
                                for i in range(int(current_tabs/4)):
                                    parsed_file.write("\t")
                                parsed_file.write('cout << "' + line[index + 1] + '" << endl;\n')
                            print_case = True
                            index += 1
                        elif word == "switch":  # switch section
                            if_case = True
                            in_loop = True
                            switch = True
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            parsed_file.write("switch (" + str(line[index + 1]) + ") {\n")
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            index += 1
                            break
                        elif word == "break":
                            for i in range(int(current_tabs/4)):
                                parsed_file.write("\t")
                            parsed_file.write("break;\n")
                            index += 1
                        elif word == "case":
                            parsed_file.write("case " + str(line[index + 1]) + ":\n")
                            index += 1
                        elif word == "//":  # comment section
                            comments = " ".join(line[1:])
                            parsed_file.write("//" + str(comments) + "\n")
                            index += 1
                            break
                        elif word == "/*":
                            block_comment = True
                            block_comment_index += 1
                            parsed_file.write("/* ")
                            index += 1
                        else:  # default case
                            if print_case:
                                print_case = False
                            else:
                                variable_name = word
                                if not in_loop and not if_case:
                                    try:
                                        test_value = None
                                        try:
                                            test_value = int(line[index + 2])
                                        except:
                                            pass
                                        if isinstance(test_value, int):
                                            for i in range(int(current_tabs/4)):
                                                parsed_file.write("\t")
                                            parsed_file.write("int ")
                                            parsed_file.write(variable_name)
                                            vars.append(variable_name)
                                        elif isinstance(line[index + 2], str):
                                            for i in range(int(current_tabs/4)):
                                                parsed_file.write("\t")
                                            parsed_file.write("string ")
                                            parsed_file.write(variable_name)
                                            end_string = True
                                            vars.append(variable_name)
                                    except IndexError:
                                        if not end_string:
                                            parsed_file.write(variable_name)
                                        else:
                                            parsed_file.write('"' + variable_name + '";\n')
                                        vars.append(variable_name)
                                else:
                                    if word not in pre_line:
                                        for i in range(int(current_tabs/4)):
                                            parsed_file.write("\t")
                                        parsed_file.write(variable_name)
                                        vars.append(variable_name)
                            index += 1
                pre_line = line
            parsed_file.write("\treturn 0;\n}")
    os.system("g++ -std=c++17 " + cpp_output[0] + ".cpp -o " + sys.argv[2])


if __name__ == "__main__":
    epal_parser()
