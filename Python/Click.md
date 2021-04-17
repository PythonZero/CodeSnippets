# Click for Python

Command line argument parser for python
- Basically example 1 does the same as example 2, but with less code

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

## Usage:

```bash
python __main__.py hello
# hello

python __main__.py whatsup
# whatsup

python __main__.py
# here are the commands you can use
# - hello
# - whatsup
```

## Requiring arguments:
```python
@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)
```

## Example of callbacks in arguments
```python
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 1.0")
    ctx.exit()


@main.command()
@click.option("--version", is_flag=True, callback=print_version, expose_value=True, is_eager=False)
def yo(version):
    x = 1
    print(f"the version is {version}")
    click.echo("Yoooo world!")  # same as print, but allows work in py2 and py3
    print(x)
```

callback allows you to change the execution order once the argument is processed.

```bash
> python __main__.py yo
The version is None
Yoooo world!
1
```

```bash
> python __main__.py yo --version
Version 1.0  # then exits.
```
