var express = require ('express');
var http = require('http');
//var httpProxy = require('http-proxy');
var fs = require('fs');
var app = express();
var PythonShell = require('python-shell');
var movie_dict_phase1 = {}; //stores movie generated for phase 1
var movie_dict_phase2 = {}; //stores movie generated for phase 2
var movie_dict_result = {}; //stores movie recommendation rating result from phase 2
var user_index = 0;
//var movie_dict_result = new Array(); //returned recommended movie list

app.use(express.static(__dirname));
app.listen(3000);

// Loading the index file . html displayed to the client
var server = http.createServer(function(req, res) {
	var pathname = require('url').parse(req.url).pathname;
	console.log("Request for " + pathname + " received.");
	//res.writeHead(200, {"Content-Type": "text/html"});
    fs.readFile(pathname.substr(1), function (err, data) {
      if (err) {
         console.log(err);
         res.writeHead(404, {'Content-Type': 'text/html'});
      }else {	
         res.writeHead(200, {'Content-Type': 'text/html'});	
         res.write(data.toString());		
      }
      res.end();
   });
});

// Loading socket.io
io = require('socket.io').listen(server);

// When a client connects, we note it in the console
io.sockets.on('connection', function(socket) {
	//socket.emit('message', 'You are connected!');
	socket.on('new_client', function(message) {
	    //create distionaries for the user
	    socket.username = message;
        movie_dict_phase1[socket.username] = new Array();
        movie_dict_phase2[socket.username] = new Array();
        movie_dict_result[socket.username] = new Array();
	});
	socket.on('message', function (message) {
        console.log(socket.username + 'is speaking to me! They are saying: ' + message);
    });
    socket.on('select_result', function (message) {
        console.log("selection result: " + message); //select result from user
        pyshell_select = new PythonShell('scripts/generate_movies.py'); //movie generation for phase 1
        pyshell_select.send(message);
        pyshell_select.on('message', function (message) {
            console.log("movie generation result for phase 1: " + message);
            temp_list = message.split("\t");
            movie_dict_phase1[socket.username].push(temp_list);
        });
        pyshell_select.end(function (err) {
            if (err) throw err;
	    socket.emit('phase2_start_page', "quiz.html");
        });
        //store select result by user
        fs.appendFile('results/phase0_result', socket.username + "\n", function (err) {
            if (err) throw err;
        });
        fs.appendFile('results/phase0_result', message + "\n", function (err) {
            if (err) throw err;
        });
    });
    socket.on('phase1_start', function (message) {
        socket.username = message;
    });
    socket.on('phase1_next', function (message) {
        var id = parseInt(message);
        console.log("asking phase 1 result for id: " + id.toString());
        console.log(movie_dict_phase2[socket.username]);
        if (movie_dict_phase1[socket.username][id] == undefined || movie_dict_phase1[socket.username][id] == null){
            socket.emit('message', "you have not completed rating or you do not have enough movie_space.");
        }
        else{
            movie_id = movie_dict_phase1[socket.username][id][0];
            movie_name = movie_dict_phase1[socket.username][id][1];
            movie_description = movie_dict_phase1[socket.username][id][2];
            movie_image = movie_dict_phase1[socket.username][id][3];

            socket.emit('movie_name', movie_name);
            socket.emit('movie_description', movie_description);
            socket.emit('movie_image', movie_image);
            socket.emit('movie_id', movie_id);
        }
    });
    socket.on('phase1_result', function (message) {
        console.log("phase 1 result: " + message);
        user_index = user_index + 1;
        pyshell_recommend = new PythonShell('scripts/recommendation.py');
        pyshell_recommend.send(message);
        pyshell_recommend.on('message', function (message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
            temp_list = message.split("\t");
            movie_dict_phase2[socket.username].push(temp_list);
        });
        pyshell_recommend.end(function (err) {
            if (err) throw err;
        });
        //store phase 1 result by user
        fs.appendFile('results/phase1_result', socket.username + "\n", function (err) {
            if (err) throw err;
        });
        fs.appendFile('results/phase1_result', message + "\n", function (err) {
            if (err) throw err;
        });
    });

    socket.on('phase2_start', function (message) {
        socket.username = message;
        movie_dict_result[socket.username] = {};
    });

    socket.on('phase2_next', function (message) {
        var id = parseInt(message);
        if (movie_dict_phase2[socket.username][id] == undefined || movie_dict_phase2[socket.username][id] == null){
            socket.emit('message', "you have not completed rating or you do not have enough movie_space.");
        }
        else{
            movie_id = movie_dict_phase2[socket.username][id][0];
            movie_name = movie_dict_phase2[socket.username][id][1];
            movie_description = movie_dict_phase2[socket.username][id][2];
            movie_image = movie_dict_phase2[socket.username][id][3];

            socket.emit('movie_name', movie_name);
            socket.emit('movie_description', movie_description);
            socket.emit('movie_image', movie_image);
            socket.emit('movie_id', movie_id);
        }
    });

    socket.on('phase2_result', function (message) {
        console.log("phase 2 result: " + message);
        temp_movie_result = JSON.parse(message);
        for (var key in temp_movie_result) {
            //console.log(temp_movie_result[key][1]);
            if (temp_movie_result.hasOwnProperty(key)) {
                movie_dict_result[socket.username][key] = new Array();
                movie_dict_result[socket.username][key].push(temp_movie_result[key][0]);
                movie_dict_result[socket.username][key].push(temp_movie_result[key][1]);
            }
        }
        var temp_Result = {};
        temp_Result[socket.username] = movie_dict_result[socket.username];
        var jsonString = JSON.stringify(temp_Result);
        fs.appendFile('results/phase2_result', jsonString + "\n", function (err) {
            if (err) throw err;
        });
    });

    socket.on('end', function (message) {
        console.log(message);
        fs.appendFile('results/uid', message + "\n", function (err) {
            if (err) throw err;
        });
    });

});
server.listen(8080);


//// Loading the index file . html displayed to the client
//var server_feedback = http.createServer(function(req, res) {
//  var pathname = require('url').parse(req.url).pathname;
//  console.log("Request for " + pathname + " received.");
//  //res.writeHead(200, {"Content-Type": "text/html"});
//    fs.readFile(pathname.substr(1), function (err, data) {
//      if (err) {
//         console.log(err);
//         res.writeHead(404, {'Content-Type': 'text/html'});
//      }else {
//         res.writeHead(200, {'Content-Type': 'text/html'});
//         res.write(data.toString());
//      }
//      res.end();
//   });
//
//});
//// Loading socket.io
//var io_feedback = require('socket.io').listen(server_feedback);
//
//// When a client connects, we note it in the console
//io_feedback.sockets.on('connection', function(socket) {
//  //socket.emit('message', 'You are connected!');
//    socket.on('feedback_start', function (message) {
//	    console.log(message);
//        socket.username = message;
//        socket.emit('message', socket.username + 'You are connected!');
//        movie_dict_result[socket.username] = {};
//    });
//    socket.on('feedback_end', function (message) {
//        //console.log(message);
//        temp_movie_result = JSON.parse(message);
//        for (var key in temp_movie_result) {
//            //console.log(temp_movie_result[key][1]);
//            if (temp_movie_result.hasOwnProperty(key)) {
//                movie_dict_result[socket.username][key] = new Array();
//                movie_dict_result[socket.username][key].push(temp_movie_result[key][0]);
//                movie_dict_result[socket.username][key].push(temp_movie_result[key][1]);
//            }
//        }
//        //pyshell_feedback = new PythonShell('feedback.py');
//	    var temp_Result = {};
//	    temp_Result[socket.username] = movie_dict_result[socket.username];
//        var jsonString = JSON.stringify(temp_Result);
//	    pyshell_feedback= new PythonShell('scripts/feedback_recommend.py');
//        pyshell_feedback.send(jsonString);
//        pyshell_feedback.on('message', function (message) {
//            console.log(message);
//        });
//        pyshell_feedback.end(function (err) {
//            if (err) throw err;
//        });
//    });
//    socket.on('next', function (message) {
//        //console.log(message);
//        var id = parseInt(message);
//        if (movie_dict_phase2[socket.username][id] == undefined || movie_dict_phase2[socket.username][id] == null){
//            socket.emit('message', "you have not completed rating or you do not have enough movie_space.");
//        }
//        else{
//            movie_id = movie_dict_phase2[socket.username][id][0];
//            movie_name = movie_dict_phase2[socket.username][id][1];
//            movie_description = movie_dict_phase2[socket.username][id][2];
//            movie_image = movie_dict_phase2[socket.username][id][3];
//            movie_url = movie_dict_phase2[socket.username][id][4];
//
//            socket.emit('movie_name', movie_name);
//            socket.emit('movie_description', movie_description);
//            socket.emit('movie_image', movie_image);
//            socket.emit('movie_url', movie_url);
//            socket.emit('movie_id', movie_id);
//        }
//    });
//    socket.on('end', function (message) {
//        console.log(message);
//	    pyshell_uid = new PythonShell('scripts/store.py');
//	    pyshell_uid.send(message);
//	    pyshell_uid.end(function (err) {
//            if (err) throw err;
//        });
//    });
//});
//server_feedback.listen(8081);
