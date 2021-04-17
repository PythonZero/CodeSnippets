# Click for Python

Basically example 1 does the same as example 2, but with less code

```python
"""Click example"""
import click


@click.group()
def main():
    pass

####################
#### EXAMPLE 1 #####
####################


@main.command()
def hello():
    print("Hello")


@main.command()
def whatsup():
    print("Whatsup")


####################
#### EXAMPLE 2 #####
####################
@click.command()
def hello():
    print("Hello")


@click.command()
def whatsup():
    print("Whatsup")

main.add_command(hello)
main.add_command(whatsup)
    
if __name__ == '__main__':
    main()
```

