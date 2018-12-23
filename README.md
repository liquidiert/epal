# epal

This is a parser for epal, your friendly, new programming language!  
epal code is easy to write and understand!  
This parser parses epal code to c++ code and compiles it to binary  
It also can be executed as pure python module  
When called in CLI, command should be like following example:
```sh
python epal_parser.py [epal_file] [binary_filename]  
```
epal will be constantly developed and is easily extendable!  
An IDE will probably provided one day!  
The .idea folder is a Pycharm project for open source development

## Why C++ as bridge?
 
I'm using C++ as bridge because it's one of the fastest 
programming languages while also having the nice abilty of OOP

## Coding example

This is an example of what epal can do up to this day (the example will change according 
to the development of epal)
```
class myfirstepalclass
        privatevar1 is 0
    public
        var1 is hallo
end 
// example comment
main 
    scur is 5
    i is 40
    do loop i 20
        if i % 2 equals 0
            scur is scur add 1
            print scur 
        end
        i is i sub 1
    end
    myclass is myfirstepalclass
    myclass.var1 is lol
    print myclass.var1
    switch scur
        case 15
            print sucess
            break
        case 1
            print noooo
            break
    end
    print scur
/* 
    and a neatly block comment
*/
```
## Syntax highlighting

Syntax highlighting is supported in Notepad++ (when using Obsidian as theme) [available as xml export](https://github.com/liquidiert/epal/blob/master/epal_syntax.xml)

![alt](https://github.com/liquidiert/epal/blob/master/.gitignore/syntax_highlighting.png "syntax highlighting")

## Upcoming features

- functions
- pointer
- references 
- typedef
- include
- enum 
- array
- lists
- try/catch
