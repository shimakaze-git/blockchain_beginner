let http = require("http");
let fs = require('fs');
let exserver = require('./server.js')

let server = http.createServer(function (req, res) {
    let url = "public" + (req.url.endsWith("/") ? req.url + "index.html" : req.url);
    console.log(url);

    if (fs.existsSync(url)) {
        if (url.split('/')[1].split('.')[1] == 'html'){
            encoding = 'UTF-8';
        } else {
            encoding = null;
        }

        fs.readFile(url, encoding,(err, data) => {
            if (!err) {
                res.writeHead(
                    200,
                    {
                        "Content-Type": exserver.getType(url)
                    }
                );
                res.write(data);
                res.end();
            } else{
                console.log(url);
            }
        });
    }
});

let port = process.env.PORT || 4000;
server.listen(port, () => {
    console.log(
        "Open URL: http://localhost:" + port
    );
});