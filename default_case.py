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
                    variables.update({variable_name: "int"})
            elif isinstance(line[index + 2], str):
                for i in range(int(current_tabs / 4)):
                    parsed_file.write("\t")
                parsed_file.write("string " + variable_name)
                loop_depth_dict.update({"end_string": True})
                if variable_name not in variables:
                    variables.update({variable_name: "string"})
        except IndexError:
            if not loop_depth_dict.get("end_string"):
                parsed_file.write(variable_name)
            else:
                parsed_file.write('"' + variable_name + '";\n')
            if variable_name not in variables:
                variables.update({variable_name: "unknown_type"})
    else:
        if word not in pre_line:
            for i in range(int(current_tabs / 4)):
                parsed_file.write("\t")
            parsed_file.write(variable_name)
            if variable_name not in variables:
                variables.update({variable_name: "unknown_type"})
    index += 1
    return True