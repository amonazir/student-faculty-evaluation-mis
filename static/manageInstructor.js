function closeResistration() {
  for (let i = 0; i < 2; i++) {
    document.getElementsByClassName("modal")[i].style.display = "none";
  }
  try {
    document.getElementsByClassName("studentDetails")[0].style.display = "none";
  } catch {
    pass;
  }
}

window.onload = function () {
  $(function () {
    $("#instructor").autocomplete({
      delay: 300,
      source: function (request, response) {
        var employee = request.term;
        $.ajax({
          url: "/duplicateEID",
          data: {
            eid: employee,
          },
          method: "POST",
          headers: {
            "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
              .value,
          },
          success: function (data) {
            $.each(data, function (key, value) {
              //   console.log(value);
              if (value == true) {
                document.getElementById("instructor").style.backgroundColor =
                  "#0000ff3b";
                document.getElementById("instructor").style.color = "white";
                document.getElementById('sbtbtn').setAttribute('enable','');
            } 
            else{
                document.getElementById('sbtbtn').setAttribute('disable','');
                document.getElementById("instructor").style.backgroundColor = "red";
            }
            });
          },
        });
      },
    });
  });
};
