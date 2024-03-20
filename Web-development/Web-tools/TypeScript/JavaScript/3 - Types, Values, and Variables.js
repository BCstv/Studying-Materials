/* JavaScript types can be divided into two categories: primitive types and object types
* PRIMITIVE                  OBJECT
*
*  Numbers                   Every thing which doesn't fall in to
*  Strings                   primitive types is automatically and object
*  Boolean
*  null                      array
*  undefined                 object
*  Symbol(ES6)               Map, Set...
* */

class Test {
    constructor(phrase) {
        this.phrase = phrase
    }
}

console.log(new Test('Hello'))

// Stores it as :Test { phrase: 'Hello'}

// JavaScript's object types are mutable and its primitive types are immutable. A value of a mutable type can change


// ---------------------------------------------------------------------------------------------------------------------

// Numbers is used to represent integers and to approximate real numbers. It uses 64-bit floating point format

let x16 = 0xBADCAFE;  // JS recognises hexadecimal numbers
console.log(x16)

let x2 = 0b1010101;  // And binary ofc
console.log(x2)

let x8 = 0o377; // JS also recognises an octal base numbers
console.log(x8)

// Floating-Point Literals [digits][.digits[p(E|e)[+|-]digits]
console.log(.333, 6.03e7, 1.9835E-5);

// Separators in Numeric Literals

let billion = 1_000_000_000
let bytes = 0x89_AB_CF_EF
let bits = 0b0001_0101_1001
let fraction = 0.12_124_49

let bigint = 1234
console.log(bigint)

console.log(BigInt(Number.MAX_SAFE_INTEGER))

// Dates and Times
let timestamp = Date.now();
let now = new Date();
let ms = now.getTime();
let iso = now.toISOString();

console.log(timestamp, now, ms, iso)

// ---------------------------------------------------------------------------------------------------------------------

// Text
let dollar = '$'
let love = '❤️'

console.log(dollar, '-', dollar.length)
console.log(love, '-', love.length)

let strange_string = `"She said 'hi'", he said.`;
console.log(strange_string)

console.log("\
one \
long \
line");


// Escape Sequences:

/* Escape Sequences:
* \0 - The NUL character
* \b - Backspace
* \t - Horizontal tab
* \n - Newline
* \v - Vertical tab
* \f - Form feed
* \r - Carriage return
* \" - Double quote
* \' - Apostrophe
* \\ - Backslash
* \xnn - The Unicode character specified by the two hexadecimal digits nn
* \unnnn - The Unicode character specified by the four hexadecimal digits nnnn
* \u{n} - The Unicode character specified by the codepoint n
* */

// Working with Strings

let s = "Hello, world!";


console.log( s.substring(1,4),
    s.slice(1,4),
    s.slice(-3),
    s.split(", "), '\n',
    // Searching a string
    s.indexOf("l"),
    s.indexOf("l", 3),
    s.indexOf("zz"),
    s.lastIndexOf("l"), '\n',
    // Boolean searching functions
    s.startsWith("Hell"),
    s.endsWith("!"),
    s.includes("o, "), '\n',
    // Creating modified versions of a string
    s.replace("llo", "ya"),
    s.toUpperCase(),
    s.toLowerCase(),
    s.normalize(),
    s.normalize("NFD"), '\n',
    // Inspecting individual characters of a string,
    s.charAt(0),
    s.charAt(s.length-1),
    s.charCodeAt(0),
    s.codePointAt(0), '\n',
    // String padding functions
    "x".padStart(3),
    "x".padEnd(3),
    "x".padStart(4, '*'),
    "x".padEnd(4, '-'), '\n',
    // Space trimming functions
    " test ".trim(),
    " test ".trimEnd(),
    " test ".trimStart(), '\n',
    // Miscellaneous string methods
    s.concat("!"),
    '<>'.repeat(5), '\n',
    // Array read-only behaviour
    s[0],
    s[s.length-1]
);

// Template Literals

let name = 'Bill';
console.log(`Hello, ${name}.`)

console.log('\n'.length)
console.log(String.raw`\n`.length)

let text = "testing: 1, 2, 3";
let pattern = /\d+/g;
console.log(pattern.test(text),
    text.search(pattern),
    text.match(pattern),
    text.replace(pattern, '#'),
    text.split(pattern))

let str_name = 'string name';
let sym_name = Symbol("propname")


// The Global Object

// Global constants like undefined, Infinity, and NaN
// Global functions like isNaN(), parseInt(), and eval()
// Constructor functions like Date(), RegExp(), String(), Object(), and Array()
// Global objects like Math like JSON

let o = { x: 1 };
o.x = 2;
o.y = 3;
console.log(o)

let a = [1, 2, 3]
a[4] = 5
a[0] = 0
console.log(a)

let x = [], b = [];  // Two distinct arrays are never equal
console.log(x === b)

console.log("4" * "8")
let smt = 1 - 'x';
console.log(smt + ' object')


console.log({1: 1}.toString())

let d = new Date(2020, 0, 12);
console.log(d.valueOf())

console.log(Number([]))


let message = "Hello";
let i= 0, j= 0, k= 0;
let v = 2, z= v**2;  // You can use previously declared variables

const H0 = 74;
const C = 299792.458;
const AU = 1.496e8;
console.log(AU)

/*When to use const?
*
* The first approach:
*   To use const only for values that are fundamentally unchanging, like the physical constants, or
*   program version numbers, or byte sequences used to identify file types
*
* The second approach:
*   Many of the so-called variables in our program don't actually ever change as our program runs.
*   We declare everything with const, and then if we find that we do actually want to allow the value
*   to vary, we switch the declaration to let.
* */

const data = [1, 2, 3, 4, 5]
for(let m = 0, len = data.length; i < len; i++) console.log('1', data[i]);
for(let datum of data) console.log('2', datum);
for(const datum of data) console.log('3', datum);

const h = 1;
if (h === 1)  {
    let h = 2;
    console.log(h)
}
// let h = 3 will raise a re-declaration error
console.log(h);

let n = 10;
n = "Hello";
/*  The difference between VAR and LET:
 !Only use var if you MUST support old browsers.!
There are few key points:

* Variables declared with var do not have block scope. Instead, they are scoped to the body of the
  containing function no matter how deeply nested they are inside that function

* If you see var outside a function body, it declares a global variable. But global variables
declared with var differ from globals declared with let in an important way. Globals declared
with var are implemented as properties of the global object
*/

for(let m = 19; m <= 25; m++) {
    console.log(m)
}

let [y, g] = [1, 2];
console.log(g);

[y, g] = [g, y];
console.log(g);

let [xx, yy] = [12e5];
console.log(xx, yy);

let [first, ...rest] = 'Hello';
console.log(first, rest);

let [aa, [bb, cc]] = [12, [42, 52], 5];

console.log(aa, bb, cc);

let [,xxx,,yyy,ccc] = [1, 2, 3, 4, 5];
console.log(xxx, yyy, ccc);


let transparent = {r: 0.0, gg:0.0, bbb: 0.0, a:1.0};

let {r, gg, bbb} = transparent

console.log(r, gg, bbb);

const {sin, cos, tan} = Math;


console.table([sin(1), cos(4), tan(4)])

function Rec_Classwork(X, Y) {
    if (X < Y) {
        console.log(X + Y);
        return (Rec_Classwork(X + 1, Y) * 2)
    }
    else if (X === Y) {
        return 1;
    }
    else {
        console.log(X + Y)
        return (Rec_Classwork(X - 1, Y) / 2)
    }
}

console.log("running a recursive function:")
console.log(Rec_Classwork(15, 10))

function Classwork(X, Y) {
    while (X !== Y) {
        console.log(X + Y);
        if (X < Y) {
            X++;
        }
        else {
            X--;
        }
    }
    return X + Y
}

console.log("running an iterative function:")
console.log(Classwork(15, 10))
