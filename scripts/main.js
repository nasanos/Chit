$(document).ready(function(){
  //Setup Materialize
  $(".button-collapse").sideNav({
    menuWidth: 200,
    closeOnClick: true,
    draggable: true,
  });
  $(".button-collapse").sideNav("show");

  //Setup Socket.IO
  namespace = "/msgs";
  var socket = io.connect(location.protocol+"//"+document.domain+":"+location.port+namespace);

  //Posting
  socket.on("chat_clear", function(usernames, msgs){
    $("#chatlog").empty();
  });
  socket.on("msgpost", function(msg){
    if (msg.data != "") {
      if (msg.username == "{{username}}") {
        $("#chatlog").append("<div id='chatp' class='card-content col s8 offset-s4 white z-depth-2'><span style='color: gray'>"+msg.username+":</span> "+msg.data+"</div>");
        $("#chatout").val("");
      } else {
        $("#chatlog").append("<div id='chatp' class='card-content col s8 white z-depth-2'><span style='color: gray'>"+msg.username+":</span> "+msg.data+"</div>");
      };
      $("#chatlog").scrollTop($("#chatlog").get(0).scrollHeight);
    };
  });

  //Forms
  $(".sidemenuopt").click(function(e) {
    socket.emit("init_chat", {data: $(e.target).text()});
  });

  $("#sending").submit(function() {
    socket.emit("msgevent", {data: $("#chatout").val()});
    return false;
  });
});