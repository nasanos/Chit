$(document).ready(function(){
  //Setup Materialize
  $(".button-collapse").sideNav({
    menuWidth: 200,
    closeOnClick: true,
    draggable: true,
  });
  $(".button-collapse").sideNav("show");

  //Menu Setup
  var usrlist = {{usrlist|safe}}
  for (var usr in usrlist) {
    if (usrlist[usr] != "{{username}}") {
      $("#slide-out").append("<li><a href='#' class='black-text sidemenuopt'>"+usrlist[usr]+"</a></li>");
    };
  };
  $("#slide-out").append("<nav id='navbottom' class='white center'><div class='nav-wrapper container'><div class='row'><a href='{{url_for("logoff")}}' class='btn right offset-s10 z-depth-1 blue darken-1 waves-effect waves-light'>Logoff</a></div></div></nav>");

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