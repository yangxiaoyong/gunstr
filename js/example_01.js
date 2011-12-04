var a = [-1, -1, 1, -3, -3, 3, 2, 2, -2, 3];
function f(s, e) {
    var ret = [];
    for (var i in s) {
        ret.push(e(s[i]));
    }
    return ret;
}

var b = f(a, function(n) { return n>0?n:0 });


