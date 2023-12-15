<h1>Compiler-Construction</h1>
<h4>Python and C++ inspire LangX. </h4>

#### [Language Specification](https://docs.google.com/document/d/1qQZOctEwxQMSBbtUT8uUzJpPKKBRQgEXpMGCxYjlFF4/edit?usp=sharing) , [Context Free Grammar](https://docs.google.com/spreadsheets/d/1CHO4TnnpyqiE1SvSEOLbCyuYNwl-7q4cV17S9-eoPxk/edit#gid=0) and [Attributed Grammar](https://docs.google.com/spreadsheets/d/1jK84-zBqsj8zFTshYl60Ty65o8W4KlT0pzxPr3-4Q4w/edit#gid=0)

<h3>Data Types and Variable Declaration</h3>
<p>Variables can be declared using <code>num dec char text bool</code> just like in C++ we use <code>int float char string bool</code> respectively.</p>

```
  num a = 10;
  text b = "two";
  bool = false;
  char = 'a';
```

<h3>Built-ins</h3>
<p>Use <code>show</code> to print anything to console.</p>

```
  print ("Hello World");
```

<h3>Conditionals</h3>
<p>LangX has when-check-otherwise block, <code>when</code> block will execute if the condition is <code>True</code>, <code>check</code> block will execute if the above condition is <code>False</code> and <code>check</code> block will execute if the condition is <code>True</code>, <code>otherwise</code> block will execute if the above conditions is <code>false</code>.

```
  num a = 10;
  when (a < 20) {
    show ("a is less than 20");
  } check (a > 15) {
      print ("a is greater than 15");
  } otherwise {
      print ("a is equals to 10");
  }
```
<h3>Loops</h3>
<p>Loop syntax we are using is the same as C++. <code>iterate</code> is used for <code>for loop</code> identification. After <code>iterate</code> we have <code>(init; cond; update;)</code>. The block will execute as long as a specified condition evaluates to true. If the condition becomes <code>false</code>, the statement within the loop stops executing and control passes to the statement following the loop. </p>

```
  iterate(num i=0; i < 10; i++){
    show("We are doing CC");
  }
```

<h3>Functions</h3>
<p>Function can be declared using <code>define</code>. A function can accept 0 to n parameters separated by comma. <code>yield</code> keyword can be used in the body to exit from function with or without a value. You can optionally specify the return type of a function</p>

```
  define isSum(a, b){
    num sum = a + b;
    when (sum == 0) {
      return "Sum is equal to Zero";
    } otherwise {
      return "Sum is greater then zero";
    }
  }
  show isSum(2,2);
```

<h3>Comments</h3>
<p>While code is for computer to understand, the comments are for humans. LangX has two types of comments i.e single-line comment, starts with <code>?</code> and multi-line comment, wrapped by <code>??...??</code>.</p>

```
  ? This is a variable
  num f = 4;
  
  ??
    This function is used to calculate age
    from date of birth.
  ??
  define calculate(dob) {
    ...
  }
```
<h3>Data Structures</h3>

<h4>Arrays</h4>
<p>The array data structure is vital in any language and LangX supports 1D array. Arrays can be defined by using <code>array</code> keyword with the dimension and collection of values inside of the brackets separated by commas. Arrays can be multi-dimensional as well.</p>

```
  array myArray[1] = [1, 2.3, 3.9, "Hellow World"];
```
<h4>Dictionary</h4>
<p>The dictionary data structure is vital in any language and LangX supports <code>dict</code>. Dict can be defined in the same way we do it in Python.</p>

```
  dict myDict = {1: "Naseem", 2: "King"}
```

## Configuration
Make `.env` file in the main directory of the project and give the following paths.
```
INPUT_FILE_PATH = ''
OUTPUT_FILE_PATH = ''
```

Install the `dotenv` package.
```
$ pip install dotenv
```

## Collaborators

The following collaborators developed this project:

- **[Muhammad Amas](https://github.com/MuhammadAmas)**
- **[Zunain Ali Azam](https://github.com/ZunainAliAzam)**
- **[Ahmed Ali](https://github.com/Ahmad43A)**

## Contributions

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
