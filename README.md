# epal

This is a parser for epal, your friendly, new programming language!
epal code is easy to write and understand!
This parser parses epal code to c++ code and compiles it to binary
It also can be executed as pure python module
When called in CLI, command should be like following example:
python epal_parser.py [epal_file] [binary_filename]
epal will be constantly developed and is easily extendable!

## Why C++ as bridge?
 
I'm using C++ as bridge because it's one of the fastest 
programming languages while also having the nice abilty of OOP

## Coding example

This is an example of what epal can do up to this day (the example will change according 
to the development of epal)
```epal
main
    scur is 5
    do loop for i in range 20
        if i % 2 equals 0
            scur is scur plus 1
            print scur
        end
    end
    switch scur
        case 15
            print sucess
            break
        case 1
            print noooo
            break
    end
    print scur
