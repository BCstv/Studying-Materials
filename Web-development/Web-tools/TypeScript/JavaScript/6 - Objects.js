let empty = {};
let point = {x: 0, y : 0};
let p2 = {x : point.x, y : point.y};
let book = {
    "main title": "JavaScript",
    "sub-title": "The Definitive Guide",
    for: "all audiences",
    author: {
        firstname: "David",
        lastname: "Flanagan"
    }
};
console.log(book);

let o = {};
let a = [];
let d = new Date();
let m = new Map();

let o1 = Object.create({x: 1, y: 2});  // o1 inherits properties x and y
console.log(o1.x + o1.y);

let o2 = Object.create(null); // to create a new object that does not have a prototype
console.log(o2);

let o3 = Object.create(Object.prototype); // To create an ordinary empty object (like object returned by {} or new Object())
console.log(o3);

// You should use Object.create when you want to guard against unintended modification of an object by a library
// function that you don't have control over.

let author = book.author;
let name = author.lastname;
let title = book["main title"];

book.edition = 7;
book['main title'] = 'ECMAScript';

o = {};
o.x = 1;
let p = Object.create(o);
p.y = 2;
let q = Object.create(p);
console.log(q)
console.log(q.x + q.y)
console.log()










