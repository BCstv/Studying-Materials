// Statement

let cx = Math.cos(2);  // It requires a whole line only for this
delete cx.cos;  // Even tho it doesn't exist
console.log(cx); // And it's a statement too

// Compound Statement

{
    let PI = Math.PI;
    cx = Math.cos(3);
    console.log("cos(п) = ", + cx);
}  // The block itself doesn't use semicolon
// console.log(PI) Will raise an error because PI is not defined on a global scope

// Empty Statement
    ;
for(let i=0; i < 10; i++) ;  // This loop has no body, but an interpreter still reads it and not raises an error

console.log(cx)
if ((2 === 0) || (1 === 0)) /* empty */ ;  // To make it clear

let username;

if (username == null) {
    let username = 'John';  // Declared a local variable
}
else
    username = 'Johny'

console.log(username)
username = 'Johny'

let i, j, k;
i = j = 1;
k = 2;

if (i === j)
    if (j === k)
        console.log("I equals K");
else
    console.log("I doesn't equal J");  // WRONG!!!

// Because an interpreter actually reads this as:
if (i === j){
    if (j === k)
        console.log("I equals K");
    else
        console.log("I doesn't equal J");
}  // Which is incorrect, because an interpreter assigns an else statement to the last if

if (i === j){
    if (j === k){
        console.log("I equals K")
    }
} else {
    console.log("I doesn't equal J")
}
// So now it's fine.

let n = 1

if (n === 1) {
    // Something
} else if (n === 2) {
    // Another Something
} else {
    // hi
}

switch (n) {
    case 1:
        // Something
    case 2:
        // Another something
    default:
        // hi
}

function convert(x) {
    switch (typeof x){
        case "string":
            return Number(x)
        case "number":
            return String(x)
        default:
            return Error
    }
}

console.log(typeof convert("3"))
console.log(convert([1, 2, 3]))

let count = 1;
while(count <= 4) {
    console.log(count);
    count++;
}

do {
    console.log(count);
    count--;
} while(count > 0)

// The for loop is declared using this sample
/*
* for(initialize ; test ; increment)
*   statement
* */

for(count; count < 4; count++) {
    console.log(count)
}

function tail(o) {
    for(; o.next; o = o.next){
        console.log(o.val)
    }
}

let o = [
    1, 2, 3, 4,  5,
    6, 7, 8, 9, 10
]

console.log(o)

console.log(o.join(' '))

let sum = 0;
for(n of o) {
    sum += n
}
console.log(sum)

o = {x: 1, y: 2, z: 3};
let keys = "";
for(let k of Object.keys(o)) {
    keys += k
}
console.log(keys);

console.log(Object.keys(o));

let pairs ="";
for(let [k, v] of Object.entries(o)) {
    console.log(k, v);
}

let frequency = {};
for(let letter of 'missisippi') {
    if(frequency[letter]) {
        frequency[letter]++;
    } else {
        frequency[letter] = 1;
    }
}


console.log(frequency)
let text = "Na na na na na na na Batman!";
let wordSet = new Set(text.split(" "));
console.log(wordSet.keys());

let m = new Map([[1, "one"], [2, "one"]]);
console.log(m);

m = {x: 1, y: 2, z: 3};
for(o in m) {
    console.log(m[o])
}

// ---------------------------------------------------------------------------------------------------------------------

// Jumps

// Labeled Statements

outerLoop: for (let i = 1; i < 2; i++) {
    innerloop: for (let j = 0; j < 2; j++) {
        if (i === 1 && j === 1) {
            break outerLoop; // exit the outer loop when i is 1 and j is 1
        }
        console.log(`i: ${i}, j: ${j}`);
    }
    console.log("I will not be displayed((")
}

let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
let s = 0, success = false

computeSum: if (matrix){
    for (let x = 0; x < matrix.length; x++) {
        let row = matrix[x];
        if (!row) break computeSum;
        for (let y = 0; y < row.length; y++) {
            let cell = row[y];
            if (isNaN(cell)) break computeSum;
            s += cell;
        }
    }
}
console.log(s)

for (const vector of matrix) {
    for (const i of vector) {
        s += i;
    }
}
console.log(s)

outerLoop: for (let i = 0; i < 3; i++) {
    console.log(`Outer loop iteration ${i}`);
    innerLoop: for (let j = 0; j < 3; j++) {
        if (i === 1 && j === 1) {
            console.log("Skipping inner loop iteration with continue");
            continue outerLoop; // Continue to the next iteration of the outer loop
        }  // Of course, it was possible to write with just a break statement. But it's just an example
        console.log(`Inner loop iteration ${j}`);
    }
}

function* range(from, to){
    for (let i = from; i <= to; i++) {
        yield i;
    }
}


console.log(range(1, 4).next())

function factorial(x) {
    if (x < 0) throw new Error("x mustn't be negative!");
    let f;
    for (f = 1; x > 1; f *= x, x--) /* empty */;
    return f;
}

try {
    // Normally, this code runs from the top of the block to the bottom without problems. But it can sometimes throw an
    // exception, either directly, with a throw statement, or indirectly, by calling a method that throws an exception
}
catch (e) {
    // The statement in this block are
}
finally {
    // This block contains statements that are always executed, regardless of what happens in the try block. They are
    // executed whether the try block terminates:
    //      1) Normally, after reaching the bottom of the block
    //      2) Because of a break, continue, or return statement
    //      3) With an exception that is handled by a catch clause above
    //      4) With an uncaught exception that is still propagating
}

// factorial(-1) Will break the whole code

try {
    let n = -1;
    let f = factorial(n);
    console.log(n + "!= " + f);
} catch (ex) {
    console.log(ex);
}
finally {
    console.log('I\'m still alive');
}

// An interpreter firstly executes the catch block

// Simulate for(initialize ; test ; increment ) body;

/*
initialize;
while (test) {
    try {body ;}
    finally { increment;}
}
*/

for (i = 0; i < 5; i++){}
console.log(i)

i = 5
while(i > 0){
    try {}
    finally {i--}
}
console.log(i);


// ---------------------------------------------------------------------------------------------------------------------

// Miscellaneous Statements

/*
* with (object)
*   statement
*/

/*
with(document.forms[0]) {
    // Access form elements directly here.  For example:
    name.value = "";
    address.value = "";
    email.value = ""
}

is equal to

let f = document.forms[0];
f.name.value = "";
f.address.value = "";
f.email.value = "";
*/

// By the way, using let or const in the first example will set local variables, not changing the document's ones

const PI = Math.PI;
const TAU = 2 * PI;
function radius(r) {return PI*r**2}
export {radius, TAU, PI};






