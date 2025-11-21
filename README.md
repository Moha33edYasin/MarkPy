# README h

This is a documentation file for your custom markup language.

## Features h

**Features:** b **

* Simple and human-friendly markup
* Fully customizable through the settings file
* Supports HTML attributes, links, images, and nested markers
* Indentation-based block structure
* Easy to extend

## Syntax Overview h

**Syntax Format:** b **
Each rule in the settings file follows this format:

```
[1st mark] [tag] [2nd mark] [3rd mark] [4th mark] [key]
```

**Components:** b **

* *[1st mark]*: Required primary marker
* *[tag]*: Required HTML tag
* *[2nd mark]*: Optional additional marker
* *[3rd mark] & [4th mark]*: Optional markers for extra tag information
* *[key]*: HTML attribute associated with the 3rd/4th marks

## Examples h

### Header Example h

```
# h
```

Usage:

```
# Title
```

Becomes an h1 element.

### Bold Example h

```
**b**
```

Usage:

```
**text**
```

Produces bold text.

### Link Example h

```
[ a ] ( ) href
```

Usage:

```
[Google](https://google.com)
```

Becomes an anchor element using *href*.

##Configuration h

**Static Marks:** b **
To change the paragraph mark or line-break mark, edit the file:

```
init.py
```

**Indentation:** b **

* The module is indentation-sensitive
* Indentation defines block structure
* 1 indent = 4 spaces

## Demo Files h

Check the following for concrete usage examples:

* demo.py
* demo.txt
