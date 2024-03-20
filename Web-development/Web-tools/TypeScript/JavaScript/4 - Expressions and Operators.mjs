let sparseArray = [1,,,,,5];
console.log(sparseArray)

let p = { x: 2.3, y: -1.2};
let q = {};
q.x = 2.3; q.y = -1.2;

console.log(q === p)

let rectangle = {
    upperLeft: {x: 2, y: 2},
    lowerRight: {x: 4, y: 5}
};

let square = function (x) {return x**2;};

console.log(square(12))

let o = {x: 1, y: {z: 3}}
let a = [o, 4, [5, 6]]

console.log(a[0].y.z)
o.x = {f: 12}
console.log(a)

// Conditional Property Access

console.log(a[0].x?.f)
console.log(a[0].x?.f.t?.d)

function square_woa(x, log=2) {
    return x**log;
}


console.log(square_woa(10, 3))

let f = null, x = 0;
try {
    f++;
} catch (e) {
    x++
}

console.log(f?.x)
console.log(x)

let obj = new Object([1, 2, 3])
console.log(obj)

x = 10
let y = -x
console.log(y)

y = String("4" * "3")
console.log(typeof y, y)

y = 10
x = ~-y // ~ inverts bits
console.log(x)

let i = 1, j = ++i;  // ++ before the value changes its instance
console.log(i, j)

/* Bitwise Operators:
* & - AND
* | - OR
* ^ - XOR
* ~ - NOT
* << - Shift left
* >> - Shift right with sign
* >>> - Shift right with zero fill
* */

/* The difference between == and ===
* They both check whether two values are the same, using two different definitions of sameness:
*
* The === operator is a strict equality. It checks whether its two operands are "identical"
* The == operator is an equality operator. It checks whether its two operands are "equal"
* == may perform a type conversion
* */

x = 1; y = '1';
console.log(x == y, x === y)

let point = {x: 1, y : 2}
console.log("x" in point, '\n', "z" in point, '\n',
    "toString" in point)  // Because point inherits this method

let d = new Date()
console.log(d instanceof Object, d instanceof Number)

// && Logical AND
// || Logical OR
// ! Logical NOT

o = {x:1}
p = null
console.log(o && o.x, o || o.y)
let b;
a = 1; b = 2;
if (a === b) stop();
(a === b) && stop(); // This does the same thing

function copy(p) {
    p = p || {} // If no p was passed, create an object
    return p;
}

console.log(!(a === b)); // a === b is false, but ! makes it true

b = 0
console.log((a = b) === 0)

a = 0
d = "data".split('')
d[++a] = 'o'

console.log(d, a)

eval(`a = 2 + 3`)
console.log(a)

// The conditional operator ?:
let username = undefined
console.log("hello" + (username ? username : ' there'))

// First defined ??
let maxWidth = undefined, prefered_width = 401
console.log('The device\'s width is:', maxWidth ?? prefered_width ?? 500)

// The delete operator
o = {x: 1, y: 2, z: 3}
delete o.x
console.log(o)
console.log("x" in o)


import {PI, radius, TAU} from "./5 - Statements.mjs";

console.log(radius(2))