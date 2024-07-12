#!/usr/bin/python3
"""a module that defines the ReferItCommand class"""
from cmd import Cmd
from models import storage


class ReferItCommand(Cmd):
    """a class that defines a shell for ReferIt"""
    prompt = "(ReferIt) "

    def do_quit(self, arg):
        """Quit command to exit the shell"""
        print('Bye')
        return True

    def do_EOF(self, arg):
        """Ctrl + D to exit the shell"""
        print('Bye')
        return True

    def emptyline(self):
        """overrides the default behaviour to rerun last command when
           there is an empty line and Enter is pressed.
        """
        pass

    def do_create(self, arg):
        """Creates a new instance of a class, saves it (to the JSON file)
           and prints the id
           e.g create BaseModel
        """
        if not arg:
            return print("** class name missing **")
        cls = storage.get_cls(arg)
        if not cls:
            return print("** class doesn't exist **")
        new_obj = cls()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, arg):
        """accepts two arguments, <class name> and <obj id>
            e.g show BaseModel 1
            It prints the string representation of the object with the
            given id.
        """
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split(' ', 1)
            if not storage.get_cls(args[0]):
                return print("** class doesn't exist **")
            if len(args) != 2:
                return print('** instance id missing **')
            result = storage.get(args[0], args[1])
            print(str(result) if result else '** no instance found **')

    def do_all(self, arg):
        """works two ways:
           1. all <class name>
           2. all
           It prints the string representation of all classes or all instance
           of selected class
        """
        if not arg:
            print([str(each) for each in storage.all().values()])
        else:
            if storage.get_cls(arg):
                print([str(each) for each in storage.all(arg).values()])
            else:
                print("** class doesn't exist **")

    def do_destroy(self, arg):
        """accepts two arguments, <class name> and <obj id>
            e.g destroy BaseModel 1
            It removes an object from storage based on given id.
        """
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split(' ', 1)
            if not storage.get_cls(args[0]):
                return print("** class doesn't exist **")
            if len(args) != 2:
                return print('** instance id missing **')
            obj_to_del = storage.get(args[0], args[1])
            if not obj_to_del:
                return print('** no instance found **')
            storage.delete(obj_to_del)
            print('delete success')

    def do_update(self, arg):
        """accepts at least 4 arguments: <class name>, <obj id>, and others.
            e.g update BaseModel 1 name "example"
            It updates an object in storage based on given id.
        """
        if not arg:
            print("** class name missing **")
        else:
            args = arg.split(' ', 2)
            cls = args[0]
            if not storage.get_cls(cls):
                return print("** class doesn't exist **")
            if len(args) < 2:
                return print('** instance id missing **')
            obj_id = args[1]
            obj_to_update = storage.get(cls, obj_id)
            if not obj_to_update:
                return print('** no instance found **')
            if len(args) != 3:
                return print('** attribute name missing **')
            args = args[2].split(' ', 1)
            if len(args) != 2:
                return print('** value missing **')
            name, value = args[0], args[1]
            if name in ['id', 'created_at', 'updated_at']:
                return print(f'** can\'t update {name} **')
            if value[0] in ['\'', '"'] \
               and value[0] == value[-1]:
                value = value[1:-1]
            try:
                attrs = storage.get_cls_attr(cls)
                attr_type = str
                if name in attrs.keys():
                    attr_type = attrs[name]
                obj_to_update.__dict__[name] = attr_type(value)
            except Exception as e:
                return print(f'Error: {e}')
            storage.save()
            print('update success')

    def do_count(self, arg):
        """accepts only one argument: <class name>
           eg count BaseModel
           It returns the number of a class is storage
        """
        if not arg:
            print("** class name missing **")
        else:
            result = storage.count(arg)
            if result is None:
                return print("** class doesn't exist **")
            print(result)


if __name__ == "__main__":
    ReferItCommand().cmdloop()
