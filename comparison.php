<?php

session_start();

ini_set('max_execution_time', 300);

/* if ($_POST['usr_dfnd_tp'] == 'on'){
    
    
} */

move_uploaded_file($_FILES['original']['tmp_name'],"OUTPUTS\\v1.asc");
move_uploaded_file($_FILES['new']['tmp_name'],"OUTPUTS\\v2.asc");

echo "
<html>
    <head>

    </head>
    <body>
        <!--Running for: <span id=\"count_up\">0:0</span>-->
    </body>
    <script src=\"http://code.jquery.com/jquery-1.9.1.min.js\"></script>
    <script>
        var counter = 0;
        var timer = " . time() . "
            setInterval(function () {
            ++counter;
            if (counter >= 60){
                minutes = Math.floor((counter / 60));
                seconds = (counter - (minutes * 60));
                $('#count_up').text(minutes + ':' + seconds);
            }else{
                $('#count_up').text('0:' + counter);
            }
            
        }, 1000);
    </script>
</html>";

$which = $_POST['tebo_fab'];
// this needs to go into the sys.argv variable array

//$tmp = exec('python comparison.py test_point_' . $_POST['tp_names'] . ' ' . $which . ' 2>&1',$my_output);
$tmp = exec('python comparison.py ' . $which . ' 2>&1',$my_output);

//remove this after testing
var_dump($my_output);

exec('start .\OUTPUTS');
exec('start .\OUTPUTS');

//header ("Location: /scripts/");