# forthy
Forth and Lisp inspired, minimalistic scripting engine


## When can this be used ?

In any application which cannot be easily restarted or modified, like a large C++ project, a game, a mobile game,...
In all of theses cases, adding a scripting library like Lua can be too complicated since other scripting languages have their own types and calling convention.
In this language, there’s nothing. No literal, no default type.
So you can add anything you want. You can even choose to manually manage your memory if your language has no GC.


## How it works

This is a (very) small interpreter, which is made to be ported to about any language quite easily.
The syntax uses the same base as Forth, a stack-oriented language.
But instead of implementing all of Forth, the language also uses Lisp features like quotes and linked lists for more control.

### Forth part

Forth uses the stack directly for operations instead of local variables, which can be rather difficult at first.

Let’s take a basic example: calling a function named ```f``` three times:
```
f f f
```
That’s it. Any operation, like adding, allocating memory,... can be called simply by typing its name.

In Forth, ```f``` is called a word. Any function (or command) is named by a word.
However, since the syntax is very limited, there are almost no restrictions on words:
+, hello-world, and {} are all valid "words".

The only restricted characters are ', (, ), [, ]:
[] is used for comments (you can nest them)
' and () are used in the Lispy part of the language
Of course, you cannot use space nor new line as a part of a word either, since these characters are used to delimit them.


#### Stack

Now, what if f has parameters ? That’s where the stack comes in.
Let’s say you want to add two numbers with the word + and show the result:
```
2 3 + print
```

2 will take the value 2 and push it on the stack
3 does the same
+ will take the two values on the top of the stack, add them, and push the result on the stack
print takes the value left by + and prints it.

As you can see, 2 + 3 becomes 2 3 + and print(x) becomes x print
This is called the suffix notation.
This can be unnatural since arithmetical operations tend to use the infix notation and function calling uses prefix notation.

### Lisp part

Lisp uses lists to describe most of its data, since its syntax is made of list literals.
In Lisp, metaprogramming is done through quotes.
A quote is a value, or a piece of data, which represents code.

forthy uses the quotes and lists from Lisp to represent code in a useable way.
For example, if i want to push the "word" + on the stack without calling +, I can just quote it:
```
'+
```

If I want to push a large sequence of words, I can use quoted lists:
```
(2 3 +)
```
will push the code which evaluates into "2 3 +"

This is very useful, as it allows precise manipulation of code by the programmer without relying on any other special syntax.

For example, to define a new word:
```
(+2 2 +) define
```

This defines a word "+2" which, quite simply, adds 2.
This assumes a number is on the stack.

#### Declaring types
Forth has found a convenient way of describing the stack behaviour of defined words.
Here, the "type signature" of the word would "n - n", meaning "in: number, out: number"
This can be inserted as a comment in the definition:
```
(+2 [n - n] 2 +) define
```

You can, of course, use complete type names, or even your own abbreviations, as long as what you mean it clear (in this case, n for "number")

#### List manipulation

At its core, a linked list is either an empty list (which is written as () in forthy) or a cell containing a value and a sub list.

In forthy, the empty list is just an empty struct (a memory block with a size of 0), and the cells are 2-slot memory cells.
Thus, lists can be manipulated the same way other memory cells are managed



### Memory management:
By default, the only way to group data is by using a memory cell which can hold pointers.

This can be thought of as a simplification of structures. Any value, whether it is a string, or even a char, is manipulated by reference. This means you can store and retrieve any value from a cell.

Cells are allocated using ```alloc [num - cell]```. Whether you want to initialize them or not is up to you, but I didn’t use raw memory access in this python implementation.
To modify the contents of the cells, the instructions you can use are ```store [cell n x - cell]``` and ```retrieve [cell n - cell x]```

In languages that have manual memory management, you will need another instruction to free the cells: ```free [x - ]```
This word is useless in managed languages, unless you want to implement your own memory model.
But it is important in library code that can be used in other environments.


