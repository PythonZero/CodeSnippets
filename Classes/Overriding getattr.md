# Overriding __getattr__ for both Instance and class

## Note - use `__getattr__` NOT `__getattribute__`
* To override the `_getattr__` of a class, you need to create a metaclass

```python
class MyClassMeta(type):
    def __getattr__(cls, name):
        """Overrides the __getattr__ if being access from the class (Not instance)"""
        return "Overrided 1"


class MyClass(metaclass=EnvVarMeta):
    x = 1
    y = 2
    # z not defined
    def __getattr__(self, name):
        """Overrides the __getattr__ if being access from an instance"""
        return "Overrided 2"


if __name__ == "__main__":
    my_instance = MyClass()
    my_instance.x = 4
    print("Instances".center(30, "="))
    print(my_instance.x)
    print(my_instance.y)
    print(my_instance.z)
    print("Classes".center(30, "="))
    print(MyClass.x)
    print(MyClass.y)
    print(MyClass.z)

```

Output:
```
==========Instances===========
4
2
Overrided 2
===========Classes============
1
2
Overrided 1
```
