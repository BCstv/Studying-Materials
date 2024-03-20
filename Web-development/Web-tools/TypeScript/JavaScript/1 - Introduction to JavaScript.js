/*
JavaScript is the programming language of the web
The overwhelming majority of websites use JavaScript,
making JavaScript the most-deployed programming language in history!

Basically, JavaScript is a trademark licensed from Sun Microsystems(Oracle) used to describe Netscape(Mozilla)'s implementation of the language
Mozilla submitted the language for standardization to ECMA(the European Computer Manufacturer's Association) - and because of trademark issues,
the standardized version of the language was stuck with the awkward name "ECMAScript" (ES), which everybody was avoiding in favor of the JavaScript
Nowadays, ECMAScript is used only to refer to JavaScript's version names

In 2015, the ES6 was released what made JS not just a scripting language, but also a serious, general-purpose language suitable for large-scale software engineering
Since ES6, ECMAScript has been moved to a yearly release cadence, and versions of the language - ES2016, ES2017, ES2018...

Node.js gave to a JavaScript a full control above the whole OS - I/O files, networks, etc.
*/

// Anything following double slashes is an English-language comment
// A variable is a symbolic name for a value. Variables are declared with
let x;
let y;
// let keyword

// Types of values supported by JS:
x = 1;  // Number can be an integer or a real
x = 0.01;  // Number (real)
x = "Hello, world!";  // A string of text
x = 'JavaScript';  // Delimit strings
x = true;  // Boolean value
x = null;  //"No value"
x = undefined;  // The same as null

// Data types

// Object:
let book = {
    topic: "JavaScript",
    edition: 7
};

book.topic  // JavaScript
book["edition"]  // 7

book.author = 'David Flanagan'
book.contents = {}

console.log(book)

console.log(book.contents?.ch01?.sect1) // Conditionally access properties with '?'

// Array
let primes = [2, 3, 5, 7]
primes[0]  // 2
primes.length  // 4
primes[primes.length-1]  // == primes[4-1] => 7
primes[4] = 9;
console.log(primes)

primes[primes.length] = 10;
console.log(primes)

primes[0] = null;
console.log(primes)

let points = [
    {
        x: 0, y: 0
    },
    {
        x: 1, y: 1
    }
];
console.log(points)

let data = {
    trial1: [
        [1, 2],
        [3, 4]
    ],
    trial2: [
        [2, 3],
        [4, 5]
    ]
};
console.log(data)

// Operators:
x = 2;
y = 3;

console.log(
    x + y,
    x - y,
    x * y,
    x ** y,
    x / y,
    x % y,
    x ++,
    y--
)


let count = 0
count += 2;
count **= 3;
count %= 4;
console.log(count)



console.log(
    x === y,
    x == y,
    x !== y,
    x != y,
    x < y,
    x >= y
)
x = 'three';
y = 'two';

console.log(x < y)

function plus1(g) {
    return g += 10;
}

let z = 1;
plus1(z)
console.log(z)

z = plus1(z)
console.log(z)

const plus10 = x => x + 10
console.log(plus10(10))

const func = (x) => (x < 2 ? x ** 2 : x * 2);  // So basically it's a lambda function :)

console.log(func(1.5), func(10))

function sum(arr) {
    let result = 0;

    for(let e of arr){
        result += e
    }
    return result;
}

console.log(sum([1, 2, 3, 4]))

function factorial(n) {
    return n <= 1 ? 1 : n * factorial(n-1)  // Return (if n <= 1:  return 1. Otherwise, n * factorial(n-1))
}

console.log(factorial(4))

for (let i = 1; i <= 10; i++) {
    console.log(i)
}

class Point {
    constructor(x, y) {  // To initialize the init function
        this.x = x;
        this.y = y;
    }
    distance() {
        return Math.sqrt(
            this.x * this.y +
            this.y * this.x
        )
    }

}

let a = new Point(10, 39);
console.log(a.distance())

class DefaultMap extends Map {
    constructor(defaultValue) {
        super();
        this.DefaultValue = defaultValue;
    }

    get(key) {
        return this.has(key) ? super.get(key) : this.DefaultValue;
    }
}


let testing = new DefaultMap(0);
testing.set(10, 12);
testing.set(12);
console.log(testing.get(2))

console.log(testing.entries())

class Histogram {
    constructor() {
        this.letterCounts = new DefaultMap(0);
        this.totalLetters = 0;
    }
    add(text) {
        // Remove whitespace from the text, and convert to uppercase
        text = text.replace(/\s/g, "").toUpperCase();
        for(let character of text) {
            let count = this.letterCounts.get(character);
            this.letterCounts.set(character, count + 1);
            this.totalLetters ++;
        }
    }
    toString() {
        // Convert the Map to an array of [key, value]
        let entries = [... this.letterCounts];
        entries.sort((a, b) => {  // A function to define a sort order
            if (a[1] === b[1]) {
                return a[0] < b[0] ? -1 : 1;
            } else {
                return b[1] - a[1];
            }
        });
        for(let entry of entries) {
            entry[1] = entry[1] / this.totalLetters*100;
        }
        entries = entries.filter(entry => entry[1] >= 1);
        let lines = entries.map(
            ([l, n]) => `${l}: ${'#'.repeat(Math.round(n))} ${n.toFixed(2)}%`
        );

        // And return the concatenated lines, separated by newline characters.
        return lines.join('\n')
    }

}

// This async function creates a Histogram object, asynchronously reads chunks of text from standard input, and adds
// those chunks of text from standard input, and adds those chunks to the histogram. When it reaches the end of the
// stream, it returns this histogram
function histogramFromStdin() { // Returns a Promise
    let histogram = new Histogram();
    for (let chunk of 'Hellojsnkjbjnlskfnhglsjfjnhlwenlwknems;lbkdgokhpoiwjlknasdfsdg') {
        histogram.add(chunk);
    }
    return histogram
}

console.log(histogramFromStdin().toString());



