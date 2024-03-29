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
        console.log(row);

        markup += "<td>";
        markup += i;
        markup += "</td>";
        m += "<tr><td><i class='fas fa-question-circle'></i></td></tr>";
        sendData(i, row[0]);
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
    if (result == 'Anomaly') {
        Row.innerHTML = "<td>" + result + " <i style='color: red;font-size: larger;' class='fas fa-bug'></i></td>";
    } else {
        Row.innerHTML = "<td>" + result + " <i style='color: green;font-size: larger;' class='fas fa-shield-check'></i></td>";
    }




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
        GenerateTable({
            'data': [
                [rowinput]
            ]
        });
        sendData(0, rowinput);
        //console.log(rowinput.split(","));

    });
});

function sendData(id = 0, data) {

    $.ajax({
        url: '/api/v1',
        data: {
            'id': id,
            'featureVec': data
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
        $('#ovw').css('display', 'none');

    } else if ($('#overtag').hasClass('active')) {
        $('#bdy').css('display', 'none');
        $('#ovw').css('display', 'block');
        $('#abt').css('display', 'none');

    } else {
        $('#bdy').css('display', 'block');
        $('#abt').css('display', 'none');
        $('#ovw').css('display', 'none');
    }

});