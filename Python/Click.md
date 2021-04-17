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

Usage:

```
python __main__.py hello
# hello

python __main__.py whatsup
# whatsup

python __main__.py
# here are the commands you can use
# - hello
# - whatsup
```

Requiring arguments:
```
@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)
```
