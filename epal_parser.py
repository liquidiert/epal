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
            keep_values_safe = False
            print_case = False
            in_loop = False
            if_case = False
            switch = False
            pre_line = None
            class_declaration = False
            for line in parse_file:
                index = 0
                line = line.split()
                for word in line:
                    if re.match("[0-9]", word):  # special characters section
                        if not keep_values_safe and not in_loop:
                            value = word
                            parsed_file.write(value + ";\n")
                        elif line[index - 1] == "+" or line[index - 1] == "plus" and if_case:
                            value = word
                            parsed_file.write(value + ";\n")
                        index += 1
                    elif word == "class":  # class section
                        if line[2:] is not None:
                            class_args = line[2:]
                        else:
                            class_args = ""
                        parse_file.write("class " + line[index + 1] + " (" + class_args +
                                         ") {\n\tprivate:\n\t")  # classes are per default private
                        class_declaration = True
                        index += 1
                    elif word == "public":
                        parsed_file.write("public:\n\t")
                        index += 1
                    elif word == "main":
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
                    elif word == "modulo" or word == "%":
                        if not keep_values_safe and not if_case:
                            parsed_file.write(" % ")
                        index += 1
                    elif word == "==" or word == "equals":
                        if not keep_values_safe and not if_case:
                            parsed_file.write(" == ")
                        index += 1
                    elif word == "nequal" or word != "!=":
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
                            parsed_file.write('\tdefault:\n\tcout << "Switch case error" << endl;\n}')
                        elif class_declaration:
                            class_declaration = False
                            parsed_file.write("};\n")
                        else:
                            parsed_file.write("\t}\n")

                        keep_values_safe = False
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
                            parsed_file.write("\tfor (int " + variable_name + " = 0; " + variable_name
                                              + " < " + line[index + 5] + "; " + variable_name + "++) {\n\t")
                        else:
                            parsed_file.write("\n\twhile (" + variable_name + " < " + line[index + 5] + "{\n\t")
                        keep_values_safe = True
                        in_loop = True
                        index += 1
                    elif word == "if":  # if section
                        if_case = True
                        conditions = " ".join(line[1:])
                        conditions = conditions.replace("equals", " == ")
                        parsed_file.write("\tif (")
                        parsed_file.write(conditions)
                        parsed_file.write(") {\n\t")
                        index += 1
                    elif word == "else":
                        parsed_file.write("\telse {\n\t")
                        index += 1
                    elif word == "elif":
                        conditions = " ".join(line[1:])
                        conditions = conditions.replace("equals", " == ")
                        parsed_file.write("\t else if (" + conditions + ") {\n\t")
                        index += 1
                    elif word == "print":  # builtins
                        if line[index + 1] in vars:
                            parsed_file.write("\tcout << " + line[index + 1] + " << endl;\n")
                        else:
                            parsed_file.write('\tcout << "' + line[index + 1] + '" << endl;\n')
                        print_case = True
                        index += 1
                    elif word == "switch":  # switch section
                        keep_values_safe = True
                        if_case = True
                        in_loop = True
                        switch = True
                        parsed_file.write("switch (" + str(line[index + 1]) + ") {\n\t")
                        index += 1
                    elif word == "break":
                        parsed_file.write("\tbreak;\n")
                        index += 1
                    elif word == "case":
                        parsed_file.write("case " + str(line[index + 1]) + ":\n")
                        index += 1
                    elif word == "//":  # comment section
                        parsed_file.write("//")
                        index += 1
                    else:  # default case
                        if print_case:
                            print_case = False
                        elif not keep_values_safe:
                            variable_name = word
                            if not in_loop and not if_case:
                                try:
                                    test_value = None
                                    try:
                                        test_value = int(line[index + 2])
                                    except:
                                        pass
                                    if isinstance(test_value, int):
                                        parsed_file.write("\tint ")
                                        parsed_file.write(variable_name)
                                        vars.append(variable_name)
                                    elif isinstance(line[index + 2], str):
                                        parsed_file.write("\tchar *")
                                        parsed_file.write(variable_name)
                                        parsed_file.write("[" + str(len(word)) + "]")
                                        vars.append(variable_name)
                                except IndexError:
                                    parsed_file.write(variable_name)
                                    vars.append(variable_name)
                            else:
                                if word not in pre_line:
                                    parsed_file.write("\t" + variable_name)
                                    vars.append(variable_name)
                        index += 1
                pre_line = line
                keep_values_safe = False
            parsed_file.write("\treturn 0;\n}")
    os.system("g++ -std=c++17 " + cpp_output[0] + ".cpp -o " + sys.argv[2])
 
 
if __name__ == "__main__":
    epal_parser()
