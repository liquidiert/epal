import sys
import re
import os


def default_case(parsed_file, word, line, loop_depth_dict, variables, classes, index, current_tabs, pre_line):
    # default case
    variable_name = word
    class_case = False
    for inner_word in line:
        if inner_word in classes:
            class_case = True
    if class_case:
        parsed_file.write(line[index + 2] + " " + word + " = " + line[index + 2] + "();\n")
        return False
    elif not loop_depth_dict.get("in_loop") and not loop_depth_dict.get("if_case"):
        try:
            test_value = None
            try:
                test_value = int(line[index + 2])
            except:
                pass
            if isinstance(test_value, int):
                for i in range(int(current_tabs / 4)):
                    parsed_file.write("\t")
                parsed_file.write("int " + variable_name)
                if variable_name not in variables:
                    variables.append(variable_name)
            elif isinstance(line[index + 2], str):
                for i in range(int(current_tabs / 4)):
                    parsed_file.write("\t")
                parsed_file.write("string " + variable_name)
                loop_depth_dict.update({"end_string": True})
                if variable_name not in variables:
                    variables.append(variable_name)
        except IndexError:
            if not loop_depth_dict.get("end_string"):
                parsed_file.write(variable_name)
            else:
                parsed_file.write('"' + variable_name + '";\n')
            if variable_name not in variables:
                variables.append(variable_name)
    else:
        if word not in pre_line:
            for i in range(int(current_tabs / 4)):
                parsed_file.write("\t")
            parsed_file.write(variable_name)
            if variable_name not in variables:
                variables.append(variable_name)
    index += 1
    return True


def epal_parser(filename):
    if filename is not None:
        args = [filename, filename.split(".")[0]]
    else:
        args = sys.argv[1:]
    variables = []
    classes = []
    functions = []
    loop_depth_dict = {}
    with open(args[0], 'r') as parse_file:
        with open("what.cpp", 'w+') as parsed_file:
            parsed_file.write("#include <iostream>\nusing namespace std;\n")
            pre_line = None
            block_comment_index = 0
            current_tabs = 0
            for line in parse_file:
                index = 0
                line = line.split()
                if loop_depth_dict.get("block_comment"):
                    if "end" in line:
                        parsed_file.write("*/\n")
                        loop_depth_dict.update({"block_comment": False})
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
                            operator = line[index - 1]
                            if not loop_depth_dict.get("in_loop"):
                                value = word
                                parsed_file.write(value + ";\n")
                            elif operator == "+" or operator == "add" or operator == "-" or operator == "sub" \
                                    or operator == "*" or operator == "mul" or operator == "/" or operator == "div" \
                                    or operator == "%" or operator == "mod" or operator == "is" or operator == "=" \
                                    and loop_depth_dict.get("if_case"):
                                value = word
                                parsed_file.write(value + ";\n")
                            index += 1
                        elif len(word) == 1:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif word == "=":  # operators
                                parsed_file.write(" = ")
                                index += 1
                            elif word == "+":
                                parsed_file.write(" + ")
                                index += 1
                            elif word == "-":
                                parsed_file.write(" - ")
                                index += 1
                            elif word == "*":
                                parsed_file.write(" * ")
                                index += 1
                            elif word == "/":
                                parsed_file.write(" / ")
                                index += 1
                            elif word == "%":
                                if not loop_depth_dict.get("if_case"):
                                    parsed_file.write(" % ")
                                index += 1
                            else:
                                if default_case(parsed_file, word, line, loop_depth_dict, variables,
                                                classes, index, current_tabs, pre_line) is False:
                                    break

                        elif len(word) == 2:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif word == "is":  # operators
                                parsed_file.write(" = ")
                                index += 1
                            elif word == "==":
                                if not loop_depth_dict.get("if_case"):
                                    parsed_file.write(" == ")
                                index += 1
                            elif word == "!=":
                                parsed_file.write(" != ")
                                index += 1
                            elif word == "&&":
                                parsed_file.write(" && ")
                                index += 1
                            elif word == "or" or word == "||":
                                parsed_file.write("||")
                                index += 1
                            elif word == "if":  # if section
                                loop_depth_dict.update({"if_case": True})
                                conditions = " ".join(line[1:])
                                conditions = conditions.replace("equals", " == ")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                parsed_file.write("if (")
                                parsed_file.write(conditions)
                                parsed_file.write(") {\n")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                index += 1
                                break
                            elif word == "//":  # comment section
                                comments = " ".join(line[1:])
                                parsed_file.write("//" + str(comments) + "\n")
                                index += 1
                                break
                            elif word == "/*":
                                loop_depth_dict.update({"block_comment": True})
                                block_comment_index += 1
                                parsed_file.write("/* ")
                                index += 1
                            elif word == "do":  # useless words
                                index += 1
                            elif word == "in":
                                index += 1
                            else:
                                if default_case(parsed_file, word, line, loop_depth_dict, variables,
                                                classes, index, current_tabs, pre_line) is False:
                                    break

                        elif len(word) == 3:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif word == "add":
                                parsed_file.write(" + ")
                                index += 1
                            elif word == "sub":
                                parsed_file.write(" - ")
                                index += 1
                            elif word == "mul":
                                parsed_file.write(" * ")
                                index += 1
                            elif word == "div":
                                parsed_file.write(" / ")
                                index += 1
                            elif word == "mod":
                                if not loop_depth_dict.get("if_case"):
                                    parsed_file.write(" % ")
                                index += 1
                            elif word == "and":
                                parsed_file.write(" && ")
                                index += 1
                            elif word == "end":
                                if loop_depth_dict.get("switch_case"):
                                    loop_depth_dict.update({"switch_case": False})
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                    parsed_file.write('default:\n\tcout << "Switch case error" << endl;\n}\n')
                                elif loop_depth_dict.get("class_declaration"):
                                    loop_depth_dict.update({"class_declaration": False})
                                    parsed_file.write("};\n")
                                elif loop_depth_dict.get("in_loop"):
                                    parsed_file.write("}\n")
                                    loop_depth_dict.update({"in_loop": False})
                                elif loop_depth_dict.get("if_case"):
                                    parsed_file.write("}\n")
                                    loop_depth_dict.update({"if_case": False})
                                else:
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                    parsed_file.write("}\n")
                                current_tabs = 0
                                index += 1
                            elif word == "tyb" or word == "try":  # try/catch section
                                parsed_file.write("try{\n")
                                break
                            elif word == "cfh":
                                exception_e = None
                                if line[index + 1:] != "":
                                    exception_e = line[index + 1:]
                                parsed_file.write("catch (" + " ".join(exception_e) + ") {\n")
                                loop_depth_dict.update({"in_loop": True})
                                index += 1
                                break
                            elif word == "for":
                                index += 1
                            else:
                                if default_case(parsed_file, word, line, loop_depth_dict, variables,
                                                classes, index, current_tabs, pre_line) is False:
                                    break

                        elif len(word) == 4:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif word == "main":  # main section
                                parsed_file.write("int main() {\n")
                                index += 1
                            elif word == "loop":  # loop section
                                loop_value = 0
                                iter_var = None
                                for inner_word in line:
                                    try:
                                        loop_value = int(inner_word)
                                    except ValueError:
                                        pass
                                    if len(inner_word) == 1:
                                        iter_var = inner_word
                                if "for" in line:
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                    parsed_file.write("for (int " + iter_var + " = 0; " + iter_var
                                                      + " < " + str(loop_value) + "; " + iter_var + "++) {\n")
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                else:
                                    for i in range(int((current_tabs / 4))):
                                        parsed_file.write("\t")
                                    parsed_file.write("while (" + iter_var + " > " + str(loop_value) + ") {\n")
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                loop_depth_dict.update({"in_loop": True})
                                index += 1
                                break
                            elif word == "else":
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                parsed_file.write("else {\n")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                index += 1
                            elif word == "elif":
                                conditions = " ".join(line[1:])
                                conditions = conditions.replace("equals", " == ")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                parsed_file.write(" else if (" + conditions + ") {\n")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                index += 1
                            elif word == "case":
                                parsed_file.write("case " + str(line[index + 1]) + ":\n")
                                index += 1
                            else:
                                if default_case(parsed_file, word, line, loop_depth_dict, variables,
                                                classes, index, current_tabs, pre_line) is False:
                                    break

                        elif len(word) == 5:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif word == "class":  # class section
                                if not len(line[2:]) == 0:
                                    class_args = "(" + str(line[2:]) + ")"
                                else:
                                    class_args = ""
                                classes.append(line[index + 1])
                                parsed_file.write("class " + line[index + 1] + " " + class_args + " {\n")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                parsed_file.write("private:\n")  # classes are per default private
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                loop_depth_dict.update({"class_declaration": True})
                                index += 1
                                break
                            elif word == "equals":
                                if not loop_depth_dict.get("if_case"):
                                    parsed_file.write(" == ")
                                index += 1
                            elif word == "nequal":
                                parsed_file.write(" != ")
                                index += 1
                            elif word == "catch":
                                exception_e = None
                                if line[index + 1:] != "":
                                    exception_e = line[index + 1:]
                                parsed_file.write("catch (" + " ".join(exception_e) + ") {\n")
                                loop_depth_dict.update({"in_loop": True})
                                index += 1
                                break
                            elif word == "print":  # builtins
                                class_var = None
                                try:
                                    class_var = line[index + 1].split(".")[1]
                                except IndexError:
                                    pass
                                if line[index + 1] in variables:
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                    parsed_file.write("cout << " + line[index + 1] + " << endl;\n")
                                elif class_var in variables:
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                    parsed_file.write("cout << " + line[index + 1] + " << endl;\n")
                                else:
                                    for i in range(int(current_tabs / 4)):
                                        parsed_file.write("\t")
                                    parsed_file.write('cout << "' + line[index + 1] + '" << endl;\n')
                                index += 1
                                break
                            elif word == "break":
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                parsed_file.write("break;\n")
                                index += 1
                            elif word == "range":
                                index += 1
                            else:
                                if default_case(parsed_file, word, line, loop_depth_dict, variables,
                                                classes, index, current_tabs, pre_line) is False:
                                    break

                        elif len(word) == 6:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif word == "public":
                                for i in range(current_tabs):
                                    parsed_file.write("\t")
                                parsed_file.write("\npublic:\n")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                index += 1
                            elif word == "switch":  # switch section
                                loop_depth_dict.update({"if_case": True})
                                loop_depth_dict.update({"in_loop": True})
                                loop_depth_dict.update({"switch_case": True})
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                parsed_file.write("switch (" + str(line[index + 1]) + ") {\n")
                                for i in range(int(current_tabs / 4)):
                                    parsed_file.write("\t")
                                index += 1
                                break
                            else:
                                if default_case(parsed_file, word, line, loop_depth_dict, variables,
                                                classes, index, current_tabs, pre_line) is False:
                                    break

                        else:
                            if "." in word:
                                parsed_file.write(word + " ")
                            elif default_case(parsed_file, word, line, loop_depth_dict, variables,
                                            classes, index, current_tabs, pre_line) is False:
                                break
                pre_line = line
            parsed_file.write("\treturn 0;\n}")
    temp = args[0].split('.')[0]
    os.system("g++ -std=c++17 -g " + "what.cpp -o " + args[1])


if __name__ == "__main__":
    epal_parser("example.epal")
