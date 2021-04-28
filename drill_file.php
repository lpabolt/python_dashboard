<?php

session_start();

move_uploaded_file($_FILES['drill']['tmp_name'],"OUTPUTS\drill.asc");
move_uploaded_file($_FILES['cad_xy']['tmp_name'],"OUTPUTS\cad_xy.asc");

$tmp = exec('python drill_file.py 2>&1',$my_output);

var_dump($my_output);

exec('start .\OUTPUTS');
//to force open
exec('start .\OUTPUTS');

//header ("Location: /scripts/");