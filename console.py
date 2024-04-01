#!/usr/bin/python3
"""defines the console for hbnb"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

# def parseline(self, arg):
#     # print 'parseline(%s) =>' % line,
#     ret = cmd.Cmd.parseline(self, arg)
#     return ret


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """
    defines the hbnb command interpreter

    Attributes:
        prompt(str): the cmd prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """shoud not execute anything"""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """
        create <class> <key 1>=<value 2> <key 2>=<value 2>
        creates a new class instance with given key/value and print its id
        """

        try:
            if not arg:
                raise SyntaxError()
            cmd_list = arg.split(" ")

            kwargs = {}
            for i in range(1, len(cmd_list)):
                key, value = tuple(cmd_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(cmd_list[0])()
            else:
                obj = eval(cmd_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

        # cmd1 = parse(arg)
        # if len(cmd1) == 0:
        #     print("** class name missing **")
        # elif cmd1[0] not in HBNBCommand.__classes:
        #     print("** class doesn't exist **")
        # else:
        #     print(eval(cmd1[0])().id)
        #     storage.save()

    def do_show(self, arg):
        """
        prints the string rep of an instance based on
        class name and id
        """
        cmd1 = parse(arg)
        objdict = storage.all()
        if len(cmd1) == 0:
            print("** class name missing **")
        elif cmd1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(cmd1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(cmd1[0], cmd1[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(cmd1[0], cmd1[1])])

    def do_destroy(self, arg):
        """
        deletes a class instance of a given id
        """
        cmd1 = parse(arg)
        objdict = storage.all()
        if len(cmd1) == 0:
            print("** class name missing **")
        elif cmd1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(cmd1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(cmd1[0], cmd1[1]) not in objdict:
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(cmd1[0], cmd1[1])]
            storage.save()

    def do_all(self, arg):
        """
        displays string rep of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        cmd1 = parse(arg)
        if len(cmd1) > 0 and cmd1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objAll = []
            for obj in storage.all().values():
                if len(cmd1) > 0 and cmd1[0] == obj.__class__.__name__:
                    objAll.append(obj.__str__())
                elif len(cmd1) == 0:
                    objAll.append(obj.__str__())
            print(objAll)

    def do_update(self, arg):
        """
        updates an instance based on the class name and id
        """
        cmd1 = parse(arg)
        objdict = storage.all()
        if len(cmd1) == 0:
            print("** class name missing **")
            return False
        if cmd1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(cmd1) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(cmd1[0], cmd1[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(cmd1) == 2:
            print("** attribute name missing **")
            return False
        if len(cmd1) == 3:
            try:
                type(eval(cmd1[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(cmd1) == 4:
            obj = objdict["{}.{}".format(cmd1[0], cmd1[1])]
            if cmd1[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[cmd1[2]])
                obj.__dict__[cmd1[2]] = valtype(cmd1[3])
            else:
                obj.__dict__[cmd1[2]] = cmd1[3]
        elif type(eval(cmd1[2])) == dict:
            obj = objdict["{}.{}".format(cmd1[0], cmd1[1])]
            for k, v in eval(cmd1[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """
        retrieves the number of instances of a given class
        """
        cmd1 = parse(arg)
        count = 0
        for obj in storage.all().values():
            if cmd1[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
