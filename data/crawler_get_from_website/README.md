# 資料怎麼來的？

[Gist](https://gist.github.com/ABlueStudent/aabc0f9e52da9ab84972c58f7b955307)

```Javascript
let raw = Array.from(
    document.getElementById("target").getElementsByTagName("tr") // 純手工標一下ID吧 :D
).map(
    (elem) => {
        return elem.textContent.replaceAll(' ', '').split('\n').map(
            e => e.trim()
        ).filter(
            e => e != ""
        )
    }
).filter(
    e => e.length != 0
);

let table = [];
table.push(["職位", "姓名", "專長", "特別門診"]);
for (let i = 1; i < raw.length; i++) {
    if (i % 2 != 0) {
        table.push(raw[i]);
    }else {
        // table[i/2] = table[i/2].concat(raw[i]);
        table[i/2] = [table[i/2][0], raw[i][0], table[i/2][1].slice(3), raw[i][1].slice(5)];
    }
}

console.log(
    table.map(
        e=>e.join(',')
    ).join('\n')
) // csv format
```