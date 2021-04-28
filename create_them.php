<?php

session_start();

$filename = $_POST['create_prefix'] . "_" . $_FILES['create_fixout']['name'];
move_uploaded_file($_FILES['create_fixout']['tmp_name'],"OUTPUTS\\" . $filename . "");

$start_list = "";
$end_list = "";

$inc = 0;
foreach ($_POST['start'] as $line){
    if ($inc == 0){
        $start_list .= $line;
    }else{
        $start_list .= "," . $line;
    }
    $inc++;
}

$inc = 0;
foreach ($_POST['end'] as $line){
    if ($inc == 0){
        $end_list .= $line;
    }else{
        $end_list .= "," . $line;
    }
    $inc++;
}

$tmp = exec('python create_them.py ' . $filename . ' ' . $_POST['create_prefix'] . ' ' . $start_list . ' ' . $end_list . ' 2>&1',$my_output);

var_dump($my_output);

exec('start .\OUTPUTS');
//to force open
exec('start .\OUTPUTS');

//header ("Location: /scripts/");