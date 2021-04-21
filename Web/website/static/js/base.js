// ---------Responsive-navbar-active-animation-----------
function test() {
    var tabsNewAnim = $('#navbarSupportedContent');
    var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
    var activeItemNewAnim = tabsNewAnim.find('.active');
    var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    var itemPosNewAnimTop = activeItemNewAnim.position();
    var itemPosNewAnimLeft = activeItemNewAnim.position();
    $(".hori-selector").css({
        "top": itemPosNewAnimTop.top + "px",
        "left": itemPosNewAnimLeft.left + "px",
        "height": activeWidthNewAnimHeight + "px",
        "width": activeWidthNewAnimWidth + "px"
    });
    $("#navbarSupportedContent").on("click", "li", function(e) {
        $('#navbarSupportedContent ul li').removeClass("active");
        $(this).addClass('active');
        var activeWidthNewAnimHeight = $(this).innerHeight();
        var activeWidthNewAnimWidth = $(this).innerWidth();
        var itemPosNewAnimTop = $(this).position();
        var itemPosNewAnimLeft = $(this).position();
        $(".hori-selector").css({
            "top": itemPosNewAnimTop.top + "px",
            "left": itemPosNewAnimLeft.left + "px",
            "height": activeWidthNewAnimHeight + "px",
            "width": activeWidthNewAnimWidth + "px"
        });
    });
}
$(document).ready(function() {
    setTimeout(function() { test(); });
});
$(window).on('resize', function() {
    setTimeout(function() { test(); }, 500);
});
$(".navbar-toggler").click(function() {
    setTimeout(function() { test(); });
});


function GenerateTable(results) {
    var markup = "";
    var m = "";
    var data = results.data;
    console.log(data);
    for (i = 0; i < data.length; i++) {
        markup += "<tr>";
        var row = data[i];
        //console.log(row);

        markup += "<td>";
        markup += i;
        markup += "</td>";
        m += "<tr><td><i class='fas fa-question-circle'></i></td></tr>";
        var cells = row.join(",").split(",");
        for (j = 0; j < cells.length; j++) {
            markup += "<td>";
            markup += cells[j];
            markup += "</td>";
        }
        markup += "</tr>";
    }

    $("#myTableR").html(m);
    $("#myTable").html(markup);
}

function CreateCell(id, result) {

    var Row = document.getElementById("myTableR").rows[id];
    var x = Row.insertCell(0);
    x.innerHTML = result;
}

var file = document.getElementById('file');
file.addEventListener('change', function() {
    var reader = new FileReader();
    var f = file.files[0];
    reader.onload = function(e) {

        $('#file').parse({
            config: {
                delimiter: "auto",
                complete: GenerateTable,
            },
            before: function(file, inputElem) {
                //console.log("Parsing file...", file);
            },
            error: function(err, file) {
                //console.log("ERROR:", err, file);
            },
            complete: function() {
                //console.log("Done with all files");
            }
        });

    };
    reader.readAsText(f);
});



$(function() {

    $('#inputbtn').click(function() {

        var rowinput = $('#input').val();
        sendData(rowinput);
        //console.log(rowinput.split(","));

    });
});

function sendData(data) {

    $.ajax({
        url: '/modal',
        data: {
            'data': data
        },
        type: 'GET',
        success: function(response) {
            console.log(response);
            CreateCell(response.id, response.result);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$("nav").click(function() {
    if ($('#abouttag').hasClass('active')) {
        $('#bdy').css('display', 'none');
        $('#abt').css('display', 'block');
    } else {
        $('#bdy').css('display', 'block');
        $('#abt').css('display', 'none');
    }

});